import json
import re
import httpx
from app.config import settings


class LLMService:
    def __init__(self):
        self.api_url = settings.AI_API_URL
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL

    def _generate_from_context(self, query: str, context: str) -> dict:
        refs = []
        for line in context.split("\n"):
            if line.startswith("---") and line.endswith("---"):
                title = line.strip("- ").strip()
                if title:
                    refs.append(title)

        first_ref = refs[0] if refs else "relevant law"

        return {
            "verdict": f"Based on {first_ref}, your legal position is described below.",
            "plain_language": f"Based on the legal provisions found in the database, here is what the law says about your question: {query}\n\nThe relevant legal references found include: {', '.join(refs[:3]) if refs else 'various legal provisions'}.\n\nFor a definitive answer, please consult a qualified Pakistani lawyer who can review the specific facts of your situation.",
            "plain_urdu": f"Aapke sawal ke mutaliq qanooni hawale mil gaye hain: {', '.join(refs[:3]) if refs else 'mohtalif qanooni qawaneen'}. Barah-e-karam kisi qualified wakeel se rabta karein.",
            "steps": [
                "Note down the specific legal references mentioned above",
                "Consult a qualified lawyer in your area",
                "Visit your nearest legal aid center if you cannot afford a lawyer",
            ],
            "legal_references": refs[:5],
        }

    async def _call_llm(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://kanun.8.jugaar.ai",
                    },
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.3,
                        "max_tokens": 500,
                    },
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"].get("content", "")
                finish = data["choices"][0].get("finish_reason", "")
                if content and finish == "stop":
                    return content
        except Exception as e:
            print(f"[LLM] API call failed: {e}", flush=True)
        return ""

    async def generate_legal_answer(self, query: str, context: str) -> dict:
        if not context.strip():
            return {
                "verdict": "No relevant legal provisions found for this query.",
                "plain_language": "The legal database does not contain specific provisions matching your query. Please consult a qualified lawyer.",
                "plain_urdu": "Is sawal ka jawab hamari database mein nahi hai. Barah-e-karam kisi wakeel se rabta karein.",
                "steps": ["Consult a local lawyer"],
                "legal_references": [],
            }

        prompt = f"Answer briefly: {query}. Context: {context[:600]}. Reply with YES or NO then 2 sentences."
        llm_result = await self._call_llm(prompt)

        if llm_result and len(llm_result) > 20:
            return {
                "verdict": llm_result[:300],
                "plain_language": llm_result,
                "plain_urdu": "",
                "steps": ["Consult a local lawyer for specific advice"],
                "legal_references": [],
            }

        return self._generate_from_context(query, context)
