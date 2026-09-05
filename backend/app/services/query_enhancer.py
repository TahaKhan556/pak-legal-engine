import re
import httpx
from app.config import settings


LEGAL_KEYWORDS_MAP = {
    "fir": "FIR first information report criminal complaint police",
    "giraftari": "arrest detention criminal",
    "arrest": "arrest detention criminal law police",
    "bail": "bail criminal bail CrPC Section 497 498 release surety",
    "zamanat": "bail criminal surety release",
    "chori": "theft theft robbery",
    "qatal": "murder homicide",
    "jahar": "poison",
    "cybercrime": "cyber crime electronic crimes",
    "harassment": "harassment",
    "tahafuz": "protection",
    "huqooq": "rights fundamental rights",
    "adalt": "court judicial",
    "case": "case trial proceedings",
    "wakil": "lawyer advocate attorney",
    "police": "police law enforcement",
    "thana": "police station",
    "warrant": "warrant arrest warrant",
    "search": "search warrant",
    "property": "property land real estate",
    "zamin": "land property",
    "taaluqaat": "relations",
    "shadi": "marriage nikah",
    "talaq": "divorce",
    "nafaq": "maintenance allowance",
    "walidat": "custody child",
    "sauda": "contract agreement",
    "qanoon": "law legislation",
    "constitution": "constitution fundamental rights",
    "peca": "prevention of electronic crimes act",
    "ppc": "pakistan penal code",
    "crpc": "code of criminal procedure",
    "cpc": "code of civil procedure",
}


def is_roman_urdu(text: str) -> bool:
    urdu_patterns = [
        r'\b(kia|kya|hai|hain|ka|ki|ke|ko|se|me|pe|par|ne|ya|aur|lekin|phir|bhi|sirf|koi|kuch|yah|woh|ye|wo|is|us)\b',
        r'\b(mujhe|tumhe|usko|unko|humko|aapko)\b',
        r'\b(kara|kare|karo|karna|karne|karta|karti)\b',
        r'\b(sakta|sakti|sakte|chahiye|pata|nahi|na)\b',
    ]
    text_lower = text.lower()
    matches = sum(1 for p in urdu_patterns if re.search(p, text_lower))
    return matches >= 2


def extract_keywords(text: str) -> list[str]:
    text_lower = text.lower()
    keywords = []
    for key, expanded in LEGAL_KEYWORDS_MAP.items():
        if key in text_lower:
            keywords.extend(expanded.split())
    return list(set(keywords))


async def translate_to_english(query: str) -> str:
    api_url = settings.AI_API_URL
    api_key = settings.AI_API_KEY
    model = settings.AI_MODEL

    prompt = f"""Translate the following Roman Urdu legal question to English. Keep it as a natural legal question. Only return the English translation, nothing else.

Roman Urdu: {query}

English:"""

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{api_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 200,
                },
                timeout=15.0,
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return query


async def enhance_query(query: str) -> dict:
    is_urdu = is_roman_urdu(query)
    keywords = extract_keywords(query)

    if is_urdu:
        english_query = await translate_to_english(query)
    else:
        english_query = query

    keyword_query = " ".join(keywords) if keywords else english_query

    return {
        "original": query,
        "english": english_query,
        "keywords": keywords,
        "is_roman_urdu": is_urdu,
        "keyword_query": keyword_query,
        "search_queries": [english_query, keyword_query],
    }
