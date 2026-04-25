#!/usr/bin/env python3
"""
Single-command pipeline runner. Runs all 5 steps in order.
Each step is skip-safe — already completed episodes are skipped automatically.

Usage (from the pipeline/ directory):
    python run.py
"""

import subprocess
import sys
from pathlib import Path

STEPS = [
    ("Fetch episodes",       "scrape/fetchEpisodes.py"),
    ("Download audio",       "scrape/downloadAudio.py"),
    ("Transcribe episodes",  "transcribe/transcribeEpisodes.py"),
    ("Analyze episodes",     "analyze/analyzeEpisodes.py"),
    ("Aggregate analysis",   "analyze/aggregateAnalysis.py"),
    ("Consolidate entities", "analyze/consolidateEntities.py"),
    ("Set up database",      "db/setupDB.py"),
    ("Insert into database", "db/insertData.py"),
]

pipelineDir = Path(__file__).parent


def main():
    python = sys.executable
    total = len(STEPS)

    for i, (label, relPath) in enumerate(STEPS, 1):
        scriptPath = pipelineDir / relPath
        print(f"\n{'=' * 60}")
        print(f"  Step {i}/{total}: {label}")
        print(f"{'=' * 60}\n")

        result = subprocess.run([python, str(scriptPath)], cwd=str(pipelineDir))

        if result.returncode != 0:
            print(f"\nPipeline stopped at step {i}/{total} ({label}).")
            print(f"Exit code: {result.returncode}")
            sys.exit(result.returncode)

    print(f"\n{'=' * 60}")
    print("  Pipeline complete.")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
