"""
The 20-row cold check (Milestone 4).

Shows you 20 posts from labels.csv with the label hidden. You label each one
from the README definitions alone -- no tools. Your label goes in the file,
the note column gets `cold`, and if the pre-label disagreed it is recorded in
the note so the disagreement isn't lost.

    python cold_check.py            # label 20 rows
    python cold_check.py --report   # show agreement on rows already marked cold
"""

import argparse
import random

import pandas as pd

LABELS = {"e": "evidence", "x": "experience", "o": "opinion"}
CSV = "labels.csv"
N = 20
SEED = 20


def report(df):
    cold = df[df["note"].str.startswith("cold")]
    if cold.empty:
        print("No cold rows yet.")
        return
    changed = cold["note"].str.contains("AI pre-label was")
    print(f"{len(cold)} cold rows. Agreed with the AI pre-label on "
          f"{len(cold) - changed.sum()} / {len(cold)} "
          f"({(len(cold) - changed.sum()) / len(cold):.0%}).")
    for _, row in cold[changed].iterrows():
        print(f"\n  you: {row['label']}  |  {row['note']}\n  {row['text'][:200]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    df = pd.read_csv(CSV, keep_default_na=False)
    if args.report:
        report(df)
        return
    if df["note"].str.startswith("cold").any():
        print("Cold rows already exist. Use --report.")
        return

    rows = random.Random(SEED).sample(range(len(df)), N)
    print("Label each post from the definitions alone: [e]vidence, e[x]perience, [o]pinion.\n")
    for n, i in enumerate(rows, 1):
        print(f"\n{'=' * 70}\n{n}/{N}\n{'=' * 70}\n{df.at[i, 'text']}\n")
        answer = ""
        while answer not in LABELS:
            answer = input("e / x / o > ").strip().lower()
        mine, prior = LABELS[answer], df.at[i, "label"]
        df.at[i, "label"] = mine
        df.at[i, "note"] = "cold" if mine == prior else f"cold; AI pre-label was {prior}"

    df.to_csv(CSV, index=False)
    print(f"\nWrote {N} cold labels to {CSV}.")
    report(df)


if __name__ == "__main__":
    main()
