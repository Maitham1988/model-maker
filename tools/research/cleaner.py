"""
Data cleaner — processes raw scraped JSON into clean JSONL for training.

Reads from data/raw/, writes to data/clean/.
No external API dependencies (AI summarization removed for offline compatibility).
"""

import json
import os
import re
from pathlib import Path

try:
    from tqdm import tqdm
except ImportError:
    print("Missing tqdm. Install with: pip install tqdm")
    raise


class DataCleaner:
    """Clean raw scraped data and generate training-ready JSONL."""

    def __init__(self, raw_dir: str = "data/raw", clean_dir: str = "data/clean"):
        self.raw_dir = Path(raw_dir)
        self.clean_dir = Path(clean_dir)
        self.clean_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def clean_text(text: str) -> str:
        """Remove extra whitespace and normalize characters."""
        if not text:
            return ""
        text = re.sub(r"\n{2,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()

    def clean_raw_data(self) -> int:
        """Walk through raw data directory and clean files, mirroring structure."""
        print(f"[*] Cleaning raw data from {self.raw_dir}...")
        count = 0

        for root, _dirs, files in os.walk(self.raw_dir):
            for file in tqdm(files, desc="Cleaning"):
                if not file.endswith(".json"):
                    continue

                raw_p = Path(root) / file
                rel_p = raw_p.relative_to(self.raw_dir)
                clean_p = self.clean_dir / rel_p
                clean_p.parent.mkdir(parents=True, exist_ok=True)

                with open(raw_p, encoding="utf-8") as f:
                    data = json.load(f)

                content = data.get("content", "")
                cleaned = self.clean_text(content)

                if len(cleaned) > 100:
                    output = {
                        "source_url": data.get("url"),
                        "query": data.get("query"),
                        "category": data.get("category"),
                        "subcategory": data.get("subcategory"),
                        "text": cleaned,
                    }
                    with open(clean_p, "w", encoding="utf-8") as f:
                        json.dump(output, f, indent=2, ensure_ascii=False)
                    count += 1

        print(f"[*] Cleaned {count} files")
        return count

    def generate_jsonl(self, output_file: str = "fine_tuning_data.jsonl") -> int:
        """Consolidate cleaned data into a single JSONL file."""
        dest = self.clean_dir / output_file
        print(f"[*] Compiling cleaned data into {dest}...")
        count = 0

        with open(dest, "w", encoding="utf-8") as out:
            for root, _dirs, files in os.walk(self.clean_dir):
                for file in files:
                    if not file.endswith(".json") or file == output_file:
                        continue
                    with open(Path(root) / file, encoding="utf-8") as f:
                        data = json.load(f)
                        entry = {
                            "instruction": data.get("query", "Survival Procedure"),
                            "context": (
                                f"Sector: {data.get('category', 'General')} | "
                                f"Sub-Sector: {data.get('subcategory', 'Emergency')}"
                            ),
                            "response": data.get("text", ""),
                        }
                        out.write(json.dumps(entry, ensure_ascii=False) + "\n")
                        count += 1

        print(f"[*] Generated {count} entries → {dest}")
        return count


if __name__ == "__main__":
    cleaner = DataCleaner()
    cleaner.clean_raw_data()
    cleaner.generate_jsonl()
