# Research Pipeline Tools

Developer tools for gathering and processing survival/engineering training data.

**These tools require internet and external dependencies** — they are for
data-collection workflows only, NOT used by the main offline application.

## Files

| File | Purpose |
|------|---------|
| `topics.py` | 150+ survival & engineering research topics (the master catalog) |
| `scraper.py` | DuckDuckGo + trafilatura web scraper |
| `cleaner.py` | Raw data → cleaned JSONL pipeline |
| `converter.py` | Instruction/Response → ChatML format for fine-tuning |

## Usage

```bash
# 1. Scrape data for all topics
python -m tools.research.scraper

# 2. Clean raw data
python -m tools.research.cleaner

# 3. Convert to ChatML for training
python -m tools.research.converter
```

## Requirements (not in main requirements.txt)

```
httpx
trafilatura
duckduckgo-search
beautifulsoup4
tqdm
```

## Important Notes

- Scraped web content may be copyrighted — do NOT commit raw/cleaned data to git
- Always verify scraped data quality before using for training
- The `data/raw/` and `data/clean/` output directories are gitignored
