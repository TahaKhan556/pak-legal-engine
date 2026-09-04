import json
import re
import httpx
from app.config import settings


class LLMService:
    def __init__(self):
        self.api_url = settings.AI_API_URL
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL

    def _parse_llm_json(self, content: str) -> dict:
        try:
            return json.loads(content)
        except (json.JSONDecodeError, ValueError):
            pass

        patterns = [
            r'```json\s*(.*?)\s*```',
            r'```\s*(.*?)\s*```',
            r'\{[^{}]*"verdict".*?\}',
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except (json.JSONDecodeError, ValueError):
                    continue

        return {
            "verdict": content[:500],
            "plain_language": content,
            "plain_urdu": "",
            "steps": [],
            "legal_references": [],
        }

    async def generate_legal_answer(
        self,
        query: str,
        context: str,
    ) -> dict:
        if not context.strip():
            return {
                "verdict": "No relevant legal provisions found in the database for this query.",
                "plain_language": "The legal database does not contain specific provisions matching your query. Please consult a qualified lawyer for advice on this matter.",
                "plain_urdu": "Is sawal ka jawab hamari database mein dastaab nahi hai. Barah-e-karam kisi qualified wakeel se rabta karein.",
                "steps": ["Consult a local lawyer", "Visit your nearest legal aid center"],
                "legal_references": [],
            }

        prompt = f"""You are a Pakistani legal expert. Answer the user's question based ONLY on the legal context provided.

LEGAL CONTEXT:
{context}

USER QUESTION:
{query}

Respond in this EXACT JSON format (no markdown, no code blocks):
{{"verdict": "Clear YES or NO answer with one sentence explanation", "plain_language": "Detailed plain-English explanation of the legal position, 2-3 paragraphs", "plain_urdu": "Same explanation in Roman Urdu (Urdu in English script) for Pakistani citizens", "steps": ["Step 1: What to do first", "Step 2: What to do next", "Step 3: Additional step"], "legal_references": ["Reference 1", "Reference 2"]}}

Rules:
- verdict MUST start with YES or NO in capitals
- Always cite specific articles/sections from the context
- plain_urdu must be in Roman Urdu, not English
- Keep plain_language under 300 words
- Steps must be actionable and practical"""

        async with httpx.AsyncClient() as client:
            for attempt in range(3):
                try:
                    response = await client.post(
                        f"{self.api_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": self.model,
                            "messages": [
                                {"role": "system", "content": "You are a Pakistani legal expert specializing in constitutional law, criminal law, and civil law. Always respond with valid JSON."},
                                {"role": "user", "content": prompt},
                            ],
                            "temperature": 0.2,
                            "max_tokens": 1500,
                        },
                        timeout=60.0,
                    )
                    response.raise_for_status()
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    result = self._parse_llm_json(content)

                    if isinstance(result.get("verdict"), str) and len(result["verdict"]) > 10:
                        if "plain_language" not in result or not result["plain_language"]:
                            result["plain_language"] = result["verdict"]
                        if "plain_urdu" not in result:
                            result["plain_urdu"] = ""
                        if "steps" not in result or not isinstance(result["steps"], list):
                            result["steps"] = ["Consult a local lawyer for specific advice"]
                        if "legal_references" not in result:
                            result["legal_references"] = []
                        return result

                except Exception as e:
                    if attempt == 2:
                        return {
                            "verdict": "Unable to generate answer at this time.",
                            "plain_language": f"An error occurred while processing your query. Please try again later or consult a local lawyer.",
                            "plain_urdu": "Is waqt jawab dene mein masla aa raha hai. Barah-e-karam dubara koshish karein ya kisi local wakeel se rabta karein.",
                            "steps": ["Try again later", "Consult a local lawyer"],
                            "legal_references": [],
                        }

        return {
            "verdict": "Unable to generate answer at this time.",
            "plain_language": "Please try again.",
            "plain_urdu": "Dubara koshish karein.",
            "steps": [],
            "legal_references": [],
        }
