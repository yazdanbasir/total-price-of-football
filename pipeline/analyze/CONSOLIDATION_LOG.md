# Entity Consolidation Run Log

Tracks what works, what doesn't, and why — so we don't repeat mistakes.

---

## Run 1 — First attempt (too aggressive)

**Thresholds:**
- `AUTO_MERGE` = 0.92 (shared for concepts and profiles)
- `GRAY_LOW` = 0.78
- Cross-encoder: `ms-marco-MiniLM-L-6-v2`, threshold = logit > 0

**Results:**
- Concepts: 3475 → 1190 (2285 merged, 66% reduction)
- Profiles: 4973 → 3706 (1267 merged, 25% reduction)
- Concept merges: 164 auto, 7663 cross-encoder
- Profile merges: 61 auto, 1789 cross-encoder

**Bad merges found:**
- `"AC Milan"` → `"Inter Milan"` — two completely different clubs
- `"Arthur"` → `"Miralem Pjanić"` — two different people
- `"Arizona State Pension Fund"` → `"Game Changer 20"` — unrelated entities
- `"Bournemouth AFC"` → `"Watford FC"` — two different clubs
- `"10-month contract"` → `"Contract deferment"` — related but distinct concepts
- `"15-point deduction"` → `"25 pence in the pound"` — completely different concepts

**Root causes:**
1. **ms-marco cross-encoder is wrong for this task.** It's a relevance model ("is this document relevant to this query?"), not a duplicate detector. Almost any two football finance entities are "relevant" to each other, so it approved nearly everything in the gray zone.
2. **GRAY_LOW of 0.78 is too low for this domain.** All content is from the same semantic neighbourhood (football finance), so unrelated entities naturally score 0.78–0.90.
3. **No name-token guard on profiles.** "AC Milan" and "Inter Milan" have highly similar descriptions (both Italian clubs, both discussed in financial contexts), causing embedding similarity to exceed 0.92.

**Action:** Restore data by re-running `aggregateAnalysis.py`, then fix thresholds and model.

---

## Run 2 — Tightened thresholds (too conservative)

**Thresholds:**
- `AUTO_MERGE_CONCEPT` = 0.95
- `AUTO_MERGE_PROFILE` = 0.96
- `GRAY_LOW` = 0.88
- Cross-encoder: `stsb-roberta-base` (semantic similarity, scores 0–5), threshold = 3.5
- Added `shareNameToken` guard: profiles with no overlapping name tokens can't merge
- Added `sameLastName` guard: persons must share last name to be compared at all

**Results:**
- Concepts: 3475 → 3450 (25 merged, 0.7% reduction)
- Profiles: 4973 → 4969 (4 merged, 0.08% reduction)
- Zero cross-encoder merges — nothing in gray zone scored ≥3.5

**Good merges:**
- All 3pm blackout variants → one entry ✓
- CVA, EFL, LMA, FFP, VAR abbreviation/expansion swaps ✓
- Kit deal / Kit manufacturer deal ✓
- Stadium sale and leaseback / Stadium sale-leaseback ✓
- PGMOL → Professional Game Match Officials Limited ✓

**Bad merges:**
- `"Cameron Winklevoss"` → `"Tyler Winklevoss"` — twins, different people. Same last name, nearly identical descriptions (always appear in same context).

**Missed merges (known):**
- FFP / PSR — same regulation renamed, not merged
- Zero cross-encoder approvals means CROSS_THRESHOLD = 3.5 is too strict for domain synonyms

**Root causes:**
1. **CROSS_THRESHOLD = 3.5 is too strict.** stsb-roberta-base scores domain synonyms in the 2.5–3.2 range, not ≥3.5.
2. **`sameLastName` guard doesn't protect against same-surname different-people.** Winklevoss twins share a last name but are distinct individuals.

**Action:** Lower CROSS_THRESHOLD to 2.8. Add first-name check: if both names have ≥2 tokens (i.e. have a first name), they must share the first token too — catches twins/siblings.

---

## Run 3 — Cross-encoder still silent (wrong scale)

**Changes from Run 2:**
- `CROSS_THRESHOLD`: 3.5 → 2.8
- `samePersonName` guard: persons must share last name AND first name (when both have ≥2 tokens)

**Results:**
- Concepts: 3475 → 3450 (25 merged — identical to Run 2)
- Profiles: 4973 → 4971 (2 merged — Winklevoss twins fix confirmed working)
- Zero cross-encoder merges again

**Root cause discovered:**
`stsb-roberta-base` outputs **0–1** (sigmoid applied internally), not 0–5 as assumed. A threshold of 2.8 is impossible to reach. That's why the cross-encoder never fired in Runs 2 or 3.

**Diagnostic results** (stsb scores for known pairs):
- FFP vs PSR: **0.237** — model has no domain knowledge that these are the same regulation
- Administration vs Insolvency: **0.354**

**Additional finding:** FFP/PSR won't be caught even with a corrected threshold. The cross-encoder lacks domain knowledge of renamed regulations. This is a hard case that requires a different approach (see Key Lessons).

**Action:** Fix threshold to 0.7 (correct scale for 0–1 output).

---

## Run 4 — Cross-encoder working, but profile stopwords too narrow

**Changes from Run 3:**
- `CROSS_THRESHOLD`: 2.8 → 0.7 (corrected for actual 0–1 output scale)

**Results:**
- Concepts: 3475 → 3237 (238 merged)
- Profiles: 4973 → 4935 (38 merged)
- Concept merges: 31 auto, 269 cross-encoder ✓ cross-encoder finally working
- Profile merges: 2 auto, 38 cross-encoder

**Good merges:**
- Concept merges broadly look correct
- Profile: Brighton Samaritans variants ✓, PGMOL/PIF/FSG abbreviation swaps ✓, Udinese variants ✓

**Bad profile merges:**
- `"AC Milan"` → `"Inter Milan"` — "Milan" passed as shared token (city name)
- `"Bohemians Prague"` → `"SK Dukla Prague"` — "Prague" passed as shared token (city name)
- `"Club de Fútbol Pachuca"` → `"Club León"` — "Club" not in stopwords
- `"National League"` → `"National Lottery"` — "National" not in stopwords
- `"Vitória FC"` → `"Vitória Guimarães"` — "Vitória" is a city/region shared by two clubs
- `"Professional Footballers' Association (PFA)"` → `"Professional Players' Federation (PFA)"` — "Professional" not in stopwords; same acronym, different orgs

**Root cause:** `shareNameToken` stopwords list too narrow — geographic names and generic org words passing as meaningful shared tokens.

**Action:** Expand stopwords significantly (geography, generic org words). Raise CROSS_THRESHOLD to 0.75.

---

## Run 5 — In progress

**Changes from Run 4:**
- Expanded `_NAME_STOPWORDS`: added club suffixes, generic org words (club, national, professional, sports, group, capital, fund...), common geography (milan, prague, london, madrid...)
- `CROSS_THRESHOLD`: 0.7 → 0.75

**Thresholds:**
- `AUTO_MERGE_CONCEPT` = 0.95
- `AUTO_MERGE_PROFILE` = 0.96
- `GRAY_LOW` = 0.88
- Cross-encoder: `stsb-roberta-base`, threshold = 0.75

**Results:** pending

---

## Key lessons

| Lesson | Detail |
|--------|--------|
| ms-marco is wrong for dedup | It scores relevance, not identity. Use stsb-roberta-base instead. |
| Domain inflates similarity | Football finance content clusters tightly. GRAY_LOW < 0.85 catches too much noise. |
| Description overwhelms name | BGE embeddings of long descriptions can pull distinct entities (AC Milan / Inter Milan) very close. Always add name-based guards for profiles. |
| `shareNameToken` blocks profile false merges | Prevents clubs/orgs with no name overlap from merging regardless of score. |
| `sameLastName` alone insufficient for persons | Twins and siblings share surnames — need first-name agreement too when available. |
| stsb-roberta-base outputs 0–1 not 0–5 | Sigmoid is applied internally. Threshold must be in 0–1 range. 2.8 and 3.5 were both unreachable — that's why cross-encoder never fired in Runs 2–3. |
| shareNameToken stopwords must cover geography and generic org words | City names (Milan, Prague) and words like "Club", "National", "Professional" are not meaningful shared tokens for clubs/orgs. Always expand stopwords before assuming name overlap is meaningful. |
| Cross-encoder can't catch renamed regulations | FFP vs PSR scores 0.237 — model has no domain knowledge that they're the same thing. Requires a different approach (e.g. manual alias list or LLM-assisted). |
| aggregateAnalysis.py already does heavy lifting | 90/88 fuzzy threshold catches most surface variants. Consolidation only needs to handle semantic cases — expect small numbers of merges (not 66%). |
