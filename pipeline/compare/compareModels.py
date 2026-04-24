# Compares Claude Haiku vs Groq Llama 3.3 70B on 3 representative episodes.
# Measures time, estimated token cost, and output quality side by side.
# Outputs raw JSON per episode to pipeline/comparison/ and a summary report.
# Run from pipeline/: python compare/compareModels.py

import json
import os
import re
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from groq import Groq
from json_repair import repair_json

load_dotenv(Path(__file__).parent.parent / ".env")

transcriptsDir = Path(__file__).parent.parent / "transcripts"
episodesFile   = Path(__file__).parent.parent / "data" / "episodes.json"
outputDir      = Path(__file__).parent.parent / "comparison"
outputDir.mkdir(parents=True, exist_ok=True)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GROQ_API_KEY      = os.getenv("GROQ_API_KEY")

if not ANTHROPIC_API_KEY:
    raise EnvironmentError("ANTHROPIC_API_KEY not set in pipeline/.env")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not set — get a free key at console.groq.com then add GROQ_API_KEY to pipeline/.env")

anthropicClient = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
groqClient      = Groq(api_key=GROQ_API_KEY)

HAIKU_MODEL = "claude-haiku-4-5-20251001"
GROQ_MODEL  = "llama-3.3-70b-versatile"

HAIKU_INPUT_PER_M  = 0.80
HAIKU_OUTPUT_PER_M = 4.00
GROQ_INPUT_PER_M   = 0.59
GROQ_OUTPUT_PER_M  = 0.79

SYSTEM_PROMPT = """You are analyzing transcripts of "The Price of Football" podcast, hosted by Kevin Day alongside Professor Kieran Maguire (University of Liverpool) and occasional guests. The show covers football finance news: transfer fees, wages, ownership structures, financial regulations (FFP, PSR, APT), league finances, and more.

Your task is to extract structured data from a transcript segment. Return ONLY valid JSON — no commentary, no markdown, no code fences.

Extract the following:

1. **concepts** — financial or regulatory terms explained or defined on this episode. Include terms where the show gives a meaningful explanation, even partial. Be thorough — include every term that gets any explanation.
   - term: the canonical, full form of the term. If it has a common abbreviation, write "Full Name (ABBR)" — e.g. "Financial Fair Play (FFP)", "Profit and Sustainability Rules (PSR)". Never use the abbreviation alone as the term.
   - definition: a 1–3 sentence explanation derived from what was said on the show
   - timestamps: array of seconds (integers) where the term is meaningfully discussed

2. **profiles** — people, football clubs, organisations, or regulatory bodies that are meaningfully discussed (not just briefly name-dropped).
   - name: the full, standard name — e.g. "Chelsea FC" not "Chelsea", "Manchester City FC" not "Man City", "FC Barcelona" not "Barça" or "Barcelona FC". For people, use their full name. Never use nicknames, partial names, or abbreviations as the name.
   - type: one of "person", "club", "organisation", "body"
   - description: 1–2 sentence description of who/what they are and their relevance to football finance, based on the episode
   - timestamps: array of seconds (integers) where they are meaningfully discussed

3. **stories** — distinct news stories or topics covered in this episode
   - headline: short headline (max 10 words)
   - summary: 2–4 sentence summary of what was discussed
   - timestamp: integer seconds where this story begins

Normalisation rules — strictly follow these:
- One entry per entity. Do not create separate entries for the same entity under different names.
- Club names: always include the legal suffix where standard — "FC", "AFC", "United", etc. Use the form the club officially uses.
- Abbreviations: always expand to full name. "FFP" → "Financial Fair Play (FFP)".
- People: use full name, e.g. "Kieran Maguire" not "Maguire" or "Prof Maguire".

Return this exact JSON structure:
{
  "concepts": [...],
  "profiles": [...],
  "stories": [...]
}"""


def formatTranscript(segments: list) -> str:
    lines = []
    for seg in segments:
        mins = int(seg["start"]) // 60
        secs = int(seg["start"]) % 60
        lines.append(f"[{mins:02d}:{secs:02d}] {seg['text']}")
    return "\n".join(lines)


def parseResponse(rawText: str) -> tuple[dict, bool]:
    rawText = rawText.strip()
    if rawText.startswith("```"):
        rawText = rawText.split("```")[1]
        if rawText.startswith("json"):
            rawText = rawText[4:]
    rawText = rawText.strip()
    try:
        return json.loads(rawText), False
    except json.JSONDecodeError:
        repaired = repair_json(rawText)
        return json.loads(repaired), True


def runHaiku(episode: dict, transcript: dict) -> tuple[dict, dict]:
    formattedTranscript = formatTranscript(transcript["segments"])
    userMessage = f"Episode: {episode['title']}\nPublished: {episode['publishedAt'][:10]}\n\nTranscript:\n{formattedTranscript}"

    start = time.time()
    response = anthropicClient.messages.create(
        model=HAIKU_MODEL,
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": userMessage}],
    )
    elapsed = time.time() - start

    data, neededRepair = parseResponse(response.content[0].text)
    cost = (response.usage.input_tokens  / 1_000_000 * HAIKU_INPUT_PER_M +
            response.usage.output_tokens / 1_000_000 * HAIKU_OUTPUT_PER_M)

    return data, {
        "model":        HAIKU_MODEL,
        "elapsed":      round(elapsed, 1),
        "inputTokens":  response.usage.input_tokens,
        "outputTokens": response.usage.output_tokens,
        "cost":         round(cost, 5),
        "neededRepair": neededRepair,
    }


def runGroq(episode: dict, transcript: dict, maxRetries: int = 3) -> tuple[dict, dict]:
    formattedTranscript = formatTranscript(transcript["segments"])
    userMessage = f"Episode: {episode['title']}\nPublished: {episode['publishedAt'][:10]}\n\nTranscript:\n{formattedTranscript}"

    for attempt in range(maxRetries):
        try:
            start = time.time()
            response = groqClient.chat.completions.create(
                model=GROQ_MODEL,
                max_tokens=8192,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": userMessage},
                ],
            )
            elapsed = time.time() - start

            data, neededRepair = parseResponse(response.choices[0].message.content)
            cost = (response.usage.prompt_tokens     / 1_000_000 * GROQ_INPUT_PER_M +
                    response.usage.completion_tokens / 1_000_000 * GROQ_OUTPUT_PER_M)

            return data, {
                "model":        GROQ_MODEL,
                "elapsed":      round(elapsed, 1),
                "inputTokens":  response.usage.prompt_tokens,
                "outputTokens": response.usage.completion_tokens,
                "cost":         round(cost, 5),
                "neededRepair": neededRepair,
            }

        except Exception as e:
            errStr = str(e).lower()
            if "rate_limit" in errStr or "rate limit" in errStr or "429" in errStr:
                waitTime = 60 * (attempt + 1)
                print(f"    Rate limited — waiting {waitTime}s before retry {attempt + 1}/{maxRetries}...")
                time.sleep(waitTime)
            else:
                raise

    raise RuntimeError(f"Groq failed after {maxRetries} retries")


def qualityMetrics(data: dict) -> dict:
    concepts = data.get("concepts", [])
    profiles = data.get("profiles", [])
    stories  = data.get("stories",  [])

    # Bare abbreviation = term is all-caps 2-6 chars with no expansion (e.g. "FFP" instead of "Financial Fair Play (FFP)")
    bareAbbrevs = [c["term"] for c in concepts if re.match(r'^[A-Z]{2,6}$', c.get("term", "").strip())]

    # Single-word club profiles (likely truncated, e.g. "Chelsea" instead of "Chelsea FC")
    clubProfiles     = [p for p in profiles if p.get("type") == "club"]
    singleWordClubs  = [p["name"] for p in clubProfiles if len(p.get("name", "").split()) == 1]

    avgDefWords  = (sum(len(c.get("definition", "").split()) for c in concepts) / len(concepts)) if concepts else 0
    avgNameWords = (sum(len(p.get("name",       "").split()) for p in profiles) / len(profiles)) if profiles else 0

    abbrevScore  = round((1 - len(bareAbbrevs)  / len(concepts))     * 100, 1) if concepts     else 100.0
    profileScore = round((1 - len(singleWordClubs) / len(clubProfiles)) * 100, 1) if clubProfiles else 100.0

    return {
        "conceptCount":    len(concepts),
        "profileCount":    len(profiles),
        "storyCount":      len(stories),
        "abbrevScore":     abbrevScore,
        "bareAbbrevs":     bareAbbrevs,
        "profileScore":    profileScore,
        "singleWordClubs": singleWordClubs,
        "avgDefWords":     round(avgDefWords,  1),
        "avgNameWords":    round(avgNameWords, 1),
    }


def printRow(label: str, haiku, groq, fmt=str, winner="higher"):
    hv = fmt(haiku)
    gv = fmt(groq)
    if winner == "higher":
        flag = "  ★ Groq" if groq > haiku else ("  ★ Haiku" if haiku > groq else "")
    else:
        flag = "  ★ Groq" if groq < haiku else ("  ★ Haiku" if haiku < groq else "")
    print(f"  {label:<28} Haiku: {hv:<12} Groq: {gv}{flag}")


def printReport(allResults: list) -> None:
    print("\n" + "=" * 70)
    print("COMPARISON REPORT")
    print("=" * 70)

    totalHaikuCost = 0.0
    totalGroqCost  = 0.0
    totalHaikuTime = 0.0
    totalGroqTime  = 0.0

    for r in allResults:
        ep     = r["episode"]
        haiku  = r["haiku"]
        groq   = r["groq"]
        hq     = haiku["quality"]
        gq     = groq["quality"]

        print(f"\n  Episode: {ep['title'][:55]}")
        print(f"  Published: {ep['publishedAt'][:10]}")
        print()
        printRow("Time (seconds)",       haiku["elapsed"],        groq["elapsed"],        fmt=lambda x: f"{x:.1f}s", winner="lower")
        printRow("Input tokens",         haiku["inputTokens"],    groq["inputTokens"],    fmt=lambda x: f"{x:,}")
        printRow("Output tokens",        haiku["outputTokens"],   groq["outputTokens"],   fmt=lambda x: f"{x:,}")
        printRow("Estimated cost",       haiku["cost"],           groq["cost"],           fmt=lambda x: f"${x:.4f}", winner="lower")
        printRow("JSON repair needed",   haiku["neededRepair"],   groq["neededRepair"],   fmt=str, winner="lower")
        print()
        printRow("Concepts extracted",   hq["conceptCount"],      gq["conceptCount"])
        printRow("Profiles extracted",   hq["profileCount"],      gq["profileCount"])
        printRow("Stories extracted",    hq["storyCount"],        gq["storyCount"])
        printRow("Abbrev compliance %",  hq["abbrevScore"],       gq["abbrevScore"],      fmt=lambda x: f"{x}%")
        printRow("Profile name score %", hq["profileScore"],      gq["profileScore"],     fmt=lambda x: f"{x}%")
        printRow("Avg def words",        hq["avgDefWords"],       gq["avgDefWords"])
        printRow("Avg name words",       hq["avgNameWords"],      gq["avgNameWords"])

        if hq["bareAbbrevs"]:
            print(f"\n  Haiku bare abbrevs: {', '.join(hq['bareAbbrevs'][:5])}")
        if gq["bareAbbrevs"]:
            print(f"  Groq bare abbrevs:  {', '.join(gq['bareAbbrevs'][:5])}")
        if hq["singleWordClubs"]:
            print(f"  Haiku single-word clubs: {', '.join(hq['singleWordClubs'][:5])}")
        if gq["singleWordClubs"]:
            print(f"  Groq single-word clubs:  {', '.join(gq['singleWordClubs'][:5])}")

        totalHaikuCost += haiku["cost"]
        totalGroqCost  += groq["cost"]
        totalHaikuTime += haiku["elapsed"]
        totalGroqTime  += groq["elapsed"]

    n = len(allResults)
    print("\n" + "-" * 70)
    print(f"TOTALS ({n} episodes)")
    print(f"  Total cost   — Haiku: ${totalHaikuCost:.4f}   Groq: ${totalGroqCost:.4f}")
    print(f"  Total time   — Haiku: {totalHaikuTime:.0f}s        Groq: {totalGroqTime:.0f}s")

    avgHaikuEpisodeCost = totalHaikuCost / n
    avgGroqEpisodeCost  = totalGroqCost  / n
    print(f"\n  Projected cost for 730 episodes:")
    print(f"    Haiku: ${avgHaikuEpisodeCost * 730:.2f}")
    print(f"    Groq:  ${avgGroqEpisodeCost  * 730:.2f}")
    print("\n  Raw outputs saved to pipeline/comparison/")
    print("  Summary saved to pipeline/comparison/report.json")
    print("=" * 70)


# ── Main ─────────────────────────────────────────────────────────────────────

with open(episodesFile) as f:
    episodes = json.load(f)

episodesWithTranscripts = [
    e for e in episodes
    if (transcriptsDir / f"{e['youtubeID']}.json").exists()
]
n = len(episodesWithTranscripts)

testEpisodes = [
    episodesWithTranscripts[n // 10],
    episodesWithTranscripts[int(n * 0.3)],
    episodesWithTranscripts[n // 2],
    episodesWithTranscripts[int(n * 0.7)],
    episodesWithTranscripts[int(n * 0.9)],
]

print(f"Found {n} episodes with transcripts. Testing on 3:")
for ep in testEpisodes:
    print(f"  • {ep['publishedAt'][:10]}  {ep['title']}")

allResults = []

for i, episode in enumerate(testEpisodes, 1):
    youtubeID = episode["youtubeID"]
    title     = episode["title"]

    print(f"\n{'─' * 60}")
    print(f"[{i}/{len(testEpisodes)}] {title}")
    print(f"        {episode['publishedAt'][:10]}")

    with open(transcriptsDir / f"{youtubeID}.json") as f:
        transcript = json.load(f)

    print("  Running Haiku...")
    haikuData, haikuStats = runHaiku(episode, transcript)
    haikuQuality = qualityMetrics(haikuData)
    print(f"  Haiku done in {haikuStats['elapsed']}s — {haikuQuality['conceptCount']} concepts, "
          f"{haikuQuality['profileCount']} profiles, {haikuQuality['storyCount']} stories")

    with open(outputDir / f"{youtubeID}_haiku.json", "w") as f:
        json.dump({"stats": haikuStats, "quality": haikuQuality, "output": haikuData}, f, indent=2, ensure_ascii=False)

    print("  Running Groq...")
    groqData, groqStats = runGroq(episode, transcript)
    groqQuality = qualityMetrics(groqData)
    print(f"  Groq  done in {groqStats['elapsed']}s — {groqQuality['conceptCount']} concepts, "
          f"{groqQuality['profileCount']} profiles, {groqQuality['storyCount']} stories")

    with open(outputDir / f"{youtubeID}_groq.json", "w") as f:
        json.dump({"stats": groqStats, "quality": groqQuality, "output": groqData}, f, indent=2, ensure_ascii=False)

    allResults.append({
        "episode": {"youtubeID": youtubeID, "title": title, "publishedAt": episode["publishedAt"]},
        "haiku":   {**haikuStats, "quality": haikuQuality},
        "groq":    {**groqStats,  "quality": groqQuality},
    })

    if i < len(testEpisodes) - 1:
        print("  Waiting 15s before next episode...")
        time.sleep(15)

with open(outputDir / "report.json", "w") as f:
    json.dump(allResults, f, indent=2, ensure_ascii=False)

printReport(allResults)
