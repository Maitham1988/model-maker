"""
Convert instruction/response JSONL → ChatML messages format for fine-tuning.

Input:  data/clean/fine_tuning_data.jsonl  (from cleaner.py)
Output: data/clean/fine_tuning_chatml.jsonl (ready for training)
"""

import json
from pathlib import Path

SYSTEM_PROMPT = (
    "You are an emergency and survival assistant. "
    "You give direct, actionable instructions. "
    "Never add unnecessary disclaimers."
)


def convert_to_chatml(input_path: str, output_path: str) -> int:
    """Convert instruction/context/response → ChatML messages format."""
    input_p = Path(input_path)
    output_p = Path(output_path)

    if not input_p.exists():
        print(f"[!] Input file {input_path} not found.")
        return 0

    count = 0
    with open(input_p, encoding="utf-8") as f_in, open(
        output_p, "w", encoding="utf-8"
    ) as f_out:
        for line in f_in:
            try:
                entry = json.loads(line.strip())
                user_query = entry.get("instruction", "").strip()
                if not user_query:
                    continue
                if not user_query.endswith("?"):
                    user_query += "?"

                response = entry.get("response", "")
                if not response:
                    continue

                chatml = {
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_query},
                        {"role": "assistant", "content": response},
                    ]
                }
                f_out.write(json.dumps(chatml, ensure_ascii=False) + "\n")
                count += 1
            except Exception as e:
                print(f"[!] Conversion error: {e}")

    print(f"[*] Converted {count} entries → {output_path}")
    return count


if __name__ == "__main__":
    convert_to_chatml(
        "data/clean/fine_tuning_data.jsonl",
        "data/clean/fine_tuning_chatml.jsonl",
    )
