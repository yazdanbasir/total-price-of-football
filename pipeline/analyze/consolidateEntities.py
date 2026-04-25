import json
import pickle
import re
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer, CrossEncoder
from rapidfuzz import fuzz

dataDir = Path(__file__).parent.parent / "data"
cacheFile = dataDir / "embeddings_cache.pkl"

EMBED_MODEL = "BAAI/bge-base-en-v1.5"
CROSS_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
AUTO_MERGE = 0.92
GRAY_LOW = 0.78


class UnionFind:
    def __init__(self):
        self._parent = {}

    def find(self, x):
        if x not in self._parent:
            self._parent[x] = x
        if self._parent[x] != x:
            self._parent[x] = self.find(self._parent[x])
        return self._parent[x]

    def union(self, x, y):
        self._parent[self.find(x)] = self.find(y)

    def groups(self, items):
        buckets = {}
        for item in items:
            root = self.find(item)
            buckets.setdefault(root, []).append(item)
        return [g for g in buckets.values() if len(g) > 1]


def loadEmbedCache():
    if cacheFile.exists():
        with open(cacheFile, "rb") as f:
            return pickle.load(f)
    return {}


def saveEmbedCache(cache):
    with open(cacheFile, "wb") as f:
        pickle.dump(cache, f)


def embedBatch(model, texts, cache):
    missing = [t for t in texts if t not in cache]
    if missing:
        print(f"  Embedding {len(missing)} new texts...")
        vecs = model.encode(missing, show_progress_bar=True, normalize_embeddings=True)
        for text, vec in zip(missing, vecs):
            cache[text] = vec
    return np.array([cache[t] for t in texts], dtype=np.float32)


def pairScore(nameA, nameB, cosine):
    strSim = fuzz.token_sort_ratio(nameA.lower(), nameB.lower()) / 100.0
    return max(float(cosine), strSim)


def hasWomen(name):
    return bool(re.search(r"\bwomen\b", name, re.IGNORECASE))


def electCanonical(cluster, entityMap):
    return max(cluster, key=lambda name: (len(entityMap[name]["episodes"]), len(name)))


def mergeInto(target, source):
    target["definitions"] = target.get("definitions", []) + source.get("definitions", [])
    target["descriptions"] = target.get("descriptions", []) + source.get("descriptions", [])
    seen = {(e["youtubeID"], e["timestamp"]) for e in target["episodes"]}
    for ep in source["episodes"]:
        key = (ep["youtubeID"], ep["timestamp"])
        if key not in seen:
            target["episodes"].append(ep)
            seen.add(key)
    return target


def consolidateConcepts(concepts, embedModel, crossModel, cache):
    if not concepts:
        return concepts, []

    names = [c["term"] for c in concepts]
    entityMap = {c["term"]: dict(c) for c in concepts}
    texts = [
        f"{c['term']}: {c['definitions'][0]['text']}" if c["definitions"] else c["term"]
        for c in concepts
    ]

    vecs = embedBatch(embedModel, texts, cache)
    simMatrix = vecs @ vecs.T

    uf = UnionFind()
    mergeLog = []
    grayPairs = []

    n = len(names)
    for i in range(n):
        for j in range(i + 1, n):
            score = pairScore(names[i], names[j], simMatrix[i, j])
            if score >= AUTO_MERGE:
                uf.union(names[i], names[j])
                mergeLog.append({"a": names[i], "b": names[j], "score": round(score, 4), "method": "auto"})
            elif score >= GRAY_LOW:
                grayPairs.append((i, j, score))

    if grayPairs and crossModel is not None:
        print(f"  Cross-encoder checking {len(grayPairs)} gray zone concept pairs...")
        pairInputs = [(texts[i], texts[j]) for i, j, _ in grayPairs]
        ceScores = crossModel.predict(pairInputs, show_progress_bar=True)
        for (i, j, score), ceScore in zip(grayPairs, ceScores):
            if float(ceScore) > 0:
                uf.union(names[i], names[j])
                mergeLog.append({
                    "a": names[i], "b": names[j],
                    "score": round(score, 4), "ceScore": round(float(ceScore), 4),
                    "method": "cross-encoder",
                })

    toRemove = set()
    for cluster in uf.groups(names):
        canonical = electCanonical(cluster, entityMap)
        for name in cluster:
            if name != canonical:
                mergeInto(entityMap[canonical], entityMap[name])
                toRemove.add(name)

    result = [
        {"term": v["term"], "definitions": v["definitions"], "episodes": v["episodes"]}
        for k, v in entityMap.items() if k not in toRemove
    ]
    result.sort(key=lambda c: c["term"].lower())
    return result, mergeLog


def consolidateProfiles(profiles, embedModel, crossModel, cache):
    if not profiles:
        return profiles, []

    names = [p["name"] for p in profiles]
    types = [p["type"] for p in profiles]
    entityMap = {p["name"]: dict(p) for p in profiles}
    texts = [
        f"{p['name']} ({p['type']}): {p['descriptions'][0]['text']}" if p["descriptions"] else f"{p['name']} ({p['type']})"
        for p in profiles
    ]

    vecs = embedBatch(embedModel, texts, cache)
    simMatrix = vecs @ vecs.T

    uf = UnionFind()
    mergeLog = []
    grayPairs = []

    n = len(names)
    for i in range(n):
        for j in range(i + 1, n):
            if types[i] != types[j]:
                continue
            if hasWomen(names[i]) != hasWomen(names[j]):
                continue
            score = pairScore(names[i], names[j], simMatrix[i, j])
            if score >= AUTO_MERGE:
                uf.union(names[i], names[j])
                mergeLog.append({"a": names[i], "b": names[j], "score": round(score, 4), "method": "auto"})
            elif score >= GRAY_LOW:
                grayPairs.append((i, j, score))

    if grayPairs and crossModel is not None:
        print(f"  Cross-encoder checking {len(grayPairs)} gray zone profile pairs...")
        pairInputs = [(texts[i], texts[j]) for i, j, _ in grayPairs]
        ceScores = crossModel.predict(pairInputs, show_progress_bar=True)
        for (i, j, score), ceScore in zip(grayPairs, ceScores):
            if float(ceScore) > 0:
                uf.union(names[i], names[j])
                mergeLog.append({
                    "a": names[i], "b": names[j],
                    "score": round(score, 4), "ceScore": round(float(ceScore), 4),
                    "method": "cross-encoder",
                })

    toRemove = set()
    for cluster in uf.groups(names):
        canonical = electCanonical(cluster, entityMap)
        for name in cluster:
            if name != canonical:
                mergeInto(entityMap[canonical], entityMap[name])
                toRemove.add(name)

    result = [
        {"name": v["name"], "type": v["type"], "descriptions": v["descriptions"], "episodes": v["episodes"]}
        for k, v in entityMap.items() if k not in toRemove
    ]
    result.sort(key=lambda p: p["name"].lower())
    return result, mergeLog


def main():
    print("Loading models...")
    embedModel = SentenceTransformer(EMBED_MODEL)
    crossModel = CrossEncoder(CROSS_MODEL)

    cache = loadEmbedCache()

    print("\nLoading data...")
    with open(dataDir / "concepts.json") as f:
        concepts = json.load(f)
    with open(dataDir / "profiles.json") as f:
        profiles = json.load(f)

    print(f"\nConcepts before consolidation: {len(concepts)}")
    print("Processing concepts...")
    consolidatedConcepts, conceptLog = consolidateConcepts(concepts, embedModel, crossModel, cache)
    print(f"Concepts after consolidation:  {len(consolidatedConcepts)}")

    print(f"\nProfiles before consolidation: {len(profiles)}")
    print("Processing profiles...")
    consolidatedProfiles, profileLog = consolidateProfiles(profiles, embedModel, crossModel, cache)
    print(f"Profiles after consolidation:  {len(consolidatedProfiles)}")

    saveEmbedCache(cache)

    with open(dataDir / "concepts.json", "w") as f:
        json.dump(consolidatedConcepts, f, indent=2, ensure_ascii=False)

    with open(dataDir / "profiles.json", "w") as f:
        json.dump(consolidatedProfiles, f, indent=2, ensure_ascii=False)

    report = {
        "concepts": {
            "before": len(concepts),
            "after": len(consolidatedConcepts),
            "merges": conceptLog,
        },
        "profiles": {
            "before": len(profiles),
            "after": len(consolidatedProfiles),
            "merges": profileLog,
        },
    }

    with open(dataDir / "consolidationReport.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\nReport written to data/consolidationReport.json")
    print(f"  Concepts merged: {len(concepts) - len(consolidatedConcepts)}")
    print(f"  Profiles merged: {len(profiles) - len(consolidatedProfiles)}")


if __name__ == "__main__":
    main()
