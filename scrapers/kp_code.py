"""
KP Code Scraper (kpcode.kp.gov.pk)
Scrapes provincial laws from Khyber Pakhtunkhwa.
"""

import httpx
from bs4 import BeautifulSoup
import asyncio
import re
from typing import Optional


class KPCodeScraper:
    BASE_URL = "https://kpcode.kp.gov.pk"

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)

    async def close(self):
        await self.client.aclose()

    async def scrape_law_list(self, offset: int = 0) -> list[dict]:
        """Scrape paginated law list."""
        url = f"{self.BASE_URL}/homepage/list_all_law/0/15/{offset}"

        try:
            response = await self.client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            laws = []

            for row in soup.select("tr"):
                cells = row.select("td")
                if len(cells) >= 3:
                    link = cells[0].select_one("a")
                    if link:
                        law = {
                            "title": cells[0].get_text(strip=True),
                            "department": cells[1].get_text(strip=True) if len(cells) > 1 else "",
                            "year": cells[2].get_text(strip=True) if len(cells) > 2 else "",
                            "url": str(link.get("href", "")),
                        }
                        laws.append(law)

            return laws

        except Exception as e:
            print(f"Error scraping law list: {e}")
            return []

    async def scrape_law_detail(self, url: str) -> Optional[dict]:
        """Scrape detailed law information and PDF link."""
        try:
            response = await self.client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            title = soup.select_one("h1, h2, .title")
            download_link = soup.select_one("a[href*='.pdf']")

            return {
                "title": title.get_text(strip=True) if title else "",
                "pdf_url": str(download_link.get("href", "")) if download_link else "",
                "url": url,
            }

        except Exception as e:
            print(f"Error scraping detail: {e}")
            return None

    async def scrape_all(self, max_pages: int = 40) -> list[dict]:
        """Scrape all laws (572 total, ~15 per page)."""
        all_laws = []

        for page in range(max_pages):
            offset = page * 15
            print(f"Scraping page {page + 1} (offset {offset})...")
            laws = await self.scrape_law_list(offset)

            if not laws:
                break

            all_laws.extend(laws)
            await asyncio.sleep(0.5)  # Rate limiting

        return all_laws


async def main():
    scraper = KPCodeScraper()
    try:
        laws = await scraper.scrape_all()
        print(f"Total KP laws scraped: {len(laws)}")
        for law in laws[:5]:
            print(f"  - {law['title']} ({law.get('year', 'N/A')})")
    finally:
        await scraper.close()


if __name__ == "__main__":
    asyncio.run(main())
