import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Optional


class PakistanCodeScraper:
    BASE_URL = "https://pakistancode.gov.pk/english"

    async def get_latest_laws(self) -> list[dict]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.BASE_URL)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                laws = []
                for link in soup.select("a[href*='view=article'], a[href*='view=category']"):
                    title = link.get_text(strip=True)
                    url = str(link.get("href", ""))
                    if title and url:
                        laws.append({"title": title, "url": url, "source": "pakistancode"})

                return laws[:20]
        except Exception as e:
            print(f"PakistanCode scraper error: {e}")
            return []


class KPCodeScraper:
    BASE_URL = "https://kpcode.kp.gov.pk"

    async def get_latest_laws(self) -> list[dict]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.BASE_URL}/homepage/latest_more")
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                laws = []
                for row in soup.select("tr"):
                    cells = row.select("td")
                    if len(cells) >= 2:
                        link = cells[0].select_one("a")
                        if link:
                            laws.append({
                                "title": cells[0].get_text(strip=True),
                                "url": str(link.get("href", "")),
                                "source": "kpcode",
                            })

                return laws[:20]
        except Exception as e:
            print(f"KPCode scraper error: {e}")
            return []


async def run_daily_scan() -> dict:
    pk_scraper = PakistanCodeScraper()
    kp_scraper = KPCodeScraper()

    pk_laws, kp_laws = await asyncio.gather(
        pk_scraper.get_latest_laws(),
        kp_scraper.get_latest_laws(),
    )

    all_laws = pk_laws + kp_laws

    return {
        "total_found": len(all_laws),
        "sources": {
            "pakistancode": len(pk_laws),
            "kpcode": len(kp_laws),
        },
        "laws": all_laws,
    }
