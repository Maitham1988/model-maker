#!/usr/bin/env python3
"""Validate the medical Q&A training dataset."""
import json

with open("training/medical_qa_dataset.jsonl") as f:
    lines = f.readlines()

print(f"Total training examples: {len(lines)}")

langs = {}
for line in lines:
    d = json.loads(line)
    user_msg = d["messages"][1]["content"]
    if any(0x0600 < ord(c) < 0x06FF for c in user_msg):
        lang = "Arabic"
    elif any(c in "éèêëàâùûîïôç" for c in user_msg.lower()):
        lang = "French"
    elif any(c in "áéíóúñ¿¡" for c in user_msg.lower()):
        lang = "Spanish"
    elif any(c in "şğıöüçŞĞİÖÜÇ" for c in user_msg):
        lang = "Turkish"
    elif any(0x0900 < ord(c) < 0x097F for c in user_msg):
        lang = "Hindi"
    else:
        lang = "English"
    langs[lang] = langs.get(lang, 0) + 1

for l, c in sorted(langs.items(), key=lambda x: -x[1]):
    print(f"  {l}: {c}")

errors = 0
for i, line in enumerate(lines):
    try:
        d = json.loads(line)
        assert "messages" in d
        assert len(d["messages"]) == 3
        for msg in d["messages"]:
            assert "role" in msg and "content" in msg
    except Exception as e:
        print(f"ERROR on line {i+1}: {e}")
        errors += 1

if errors == 0:
    print("All entries valid JSON ✓")
else:
    print(f"{errors} errors found")
