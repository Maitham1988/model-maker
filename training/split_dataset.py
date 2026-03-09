#!/usr/bin/env python3
"""Split llama_english_medical.jsonl into train/valid/test splits."""

import json
import random
import os
from pathlib import Path

BASE = Path(__file__).parent
SRC = BASE / "llama_english_medical.jsonl"
OUT = BASE / "llama_splits"

with open(SRC) as f:
    data = [json.loads(line) for line in f]

print(f"Total examples: {len(data)}")

random.seed(42)
random.shuffle(data)

n = len(data)
n_test = max(20, int(n * 0.1))
n_valid = max(20, int(n * 0.1))
n_train = n - n_test - n_valid

splits = {
    "train": data[:n_train],
    "valid": data[n_train:n_train + n_valid],
    "test": data[n_train + n_valid:],
}

print(f"Train: {len(splits['train'])}, Valid: {len(splits['valid'])}, Test: {len(splits['test'])}")

os.makedirs(OUT, exist_ok=True)
for name, items in splits.items():
    path = OUT / f"{name}.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for ex in items:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"  {name}: {len(items)} examples -> {path}")

print("Done!")
