"""
Web scraper for survival/engineering research data.

Uses DuckDuckGo search + trafilatura for clean text extraction.
Requires: pip install httpx trafilatura duckduckgo-search beautifulsoup4 tqdm

WARNING: Scraped content may be copyrighted. Do NOT commit raw data to git.
         Always verify data quality and relevance before using for training.
"""

import json
from pathlib import Path

try:
    import trafilatura
    from duckduckgo_search import DDGS
    from tqdm import tqdm
except ImportError:
    print(
        "Missing dependencies. Install with:\n"
        "  pip install trafilatura duckduckgo-search tqdm"
    )
    raise


class ResearchScraper:
    """Search the web and extract clean article text for research topics."""

    def __init__(self, output_dir: str = "data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def search_and_scrape(
        self,
        query: str,
        category: str,
        subcategory: str,
        num_results: int = 5,
    ) -> list[str]:
        """Search DuckDuckGo and scrape clean text from top results."""
        save_path = self.output_dir / category / subcategory
        save_path.mkdir(parents=True, exist_ok=True)

        print(f"[*] Researching '{query}' in {category}/{subcategory}...")
        results: list[str] = []

        try:
            with DDGS() as ddgs:
                search_results = [
                    r["href"] for r in ddgs.text(query, max_results=num_results)
                ]
        except Exception as e:
            print(f"[!] Search failed for {query}: {e}")
            return []

        for i, url in enumerate(tqdm(search_results, desc="Scraping")):
            extracted = self._scrape_clean_text(url)
            if extracted:
                filename = f"source_{i:03d}.json"
                with open(save_path / filename, "w", encoding="utf-8") as f:
                    json.dump(
                        {
                            "url": url,
                            "query": query,
                            "content": extracted,
                            "category": category,
                            "subcategory": subcategory,
                        },
                        f,
                        indent=2,
                        ensure_ascii=False,
                    )
                results.append(url)

        return results

    @staticmethod
    def _scrape_clean_text(url: str) -> str | None:
        """Fetch URL and extract main article text via trafilatura."""
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                return trafilatura.extract(
                    downloaded, include_comments=False, include_tables=True
                )
        except Exception as e:
            print(f"[!] Error scraping {url}: {e}")
        return None


if __name__ == "__main__":
    from tools.research.topics import get_all_topics

    scraper = ResearchScraper()
    all_topics = get_all_topics()
    for category, topic_list in all_topics.items():
        for subcategory, query in topic_list:
            scraper.search_and_scrape(query, category, subcategory)
