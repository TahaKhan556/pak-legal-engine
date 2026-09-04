"""
Pakistan Code Scraper (pakistancode.gov.pk)
Scrapes federal laws from the official Ministry of Law website.
"""

import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Optional


class PakistanCodeScraper:
    BASE_URL = "https://pakistancode.gov.pk/english"

    CATEGORIES = {
        "criminal": "Criminal Laws",
        "civil": "Civil Laws",
        "family": "Family Laws",
        "service": "Service Laws",
        "labour": "Labour Laws",
        "police": "Police Laws",
        "companies": "Companies Laws",
        "land": "Land/Property Laws",
        "banking": "Banking/Financial Laws",
        "election": "Election Laws",
        "general": "General Laws",
    }

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)

    async def close(self):
        await self.client.aclose()

    async def scrape_category(self, category: str) -> list[dict]:
        """Scrape laws from a specific category."""
        url = f"{self.BASE_URL}/index.php?option=com_content&view=category&id={category}"

        try:
            response = await self.client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            laws = []

            for link in soup.select("a[href*='view=article']"):
                law = {
                    "title": link.get_text(strip=True),
                    "url": str(link.get("href", "")),
                    "category": category,
                }
                if law["title"] and law["url"]:
                    laws.append(law)

            return laws

        except Exception as e:
            print(f"Error scraping {category}: {e}")
            return []

    async def scrape_law_detail(self, url: str) -> Optional[dict]:
        """Scrape detailed information about a specific law."""
        try:
            response = await self.client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.select_one("h1, .article-title")
            content = soup.select_one(".article-content, .item-page")

            return {
                "title": title.get_text(strip=True) if title else "",
                "content": content.get_text(strip=True) if content else "",
                "url": url,
            }

        except Exception as e:
            print(f"Error scraping detail: {e}")
            return None

    async def scrape_all(self) -> list[dict]:
        """Scrape all categories."""
        all_laws = []

        for category_id, category_name in self.CATEGORIES.items():
            print(f"Scraping {category_name}...")
            laws = await self.scrape_category(category_id)
            all_laws.extend(laws)
            await asyncio.sleep(1)  # Rate limiting

        return all_laws


async def main():
    scraper = PakistanCodeScraper()
    try:
        laws = await scraper.scrape_all()
        print(f"Total laws scraped: {len(laws)}")
        for law in laws[:5]:
            print(f"  - {law['title']}")
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
