import httpx
from app.config import settings


class LLMService:
    def __init__(self):
        self.api_url = settings.AI_API_URL
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL

    async def generate_legal_answer(
        self,
        query: str,
        context: str,
    ) -> dict:
        prompt = f"""You are a Pakistani legal expert. Based on the following legal context, answer the user's question.

LEGAL CONTEXT:
{context}

USER QUESTION:
{query}

Provide your response in the following JSON format:
{{
    "verdict": "A clear YES/NO answer with brief explanation",
    "plain_language": "A detailed plain-language explanation of the legal position",
    "plain_urdu": "The same explanation in Roman Urdu for Pakistani citizens",
    "steps": ["Step 1: ...", "Step 2: ...", "Step 3: ..."],
    "legal_references": ["Article 14 of Constitution", "Section 302 PPC", ...]
}}

Important:
- Always cite specific articles, sections, and laws
- Keep the verdict clear and direct
- Provide practical, actionable steps
- Write plain_urdu in Roman Urdu (Urdu written in English script)
- If the context doesn't contain enough information, say so clearly"""

        async with httpx.AsyncClient() as client:
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
                            {"role": "system", "content": "You are a Pakistani legal expert specializing in constitutional law, criminal law, and civil law."},
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.3,
                        "max_tokens": 2000,
                    },
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()

                content = data["choices"][0]["message"]["content"]

                import json
                try:
                    result = json.loads(content)
                except json.JSONDecodeError:
                    result = {
                        "verdict": content[:200],
                        "plain_language": content,
                        "plain_urdu": "",
                        "steps": ["Consult with a local lawyer for specific advice"],
                        "legal_references": [],
                    }

                return result

            except Exception as e:
                return {
                    "verdict": "Unable to generate answer at this time",
                    "plain_language": f"Error: {str(e)}",
                    "plain_urdu": "Is waqt jawab dene mein masla aa raha hai",
                    "steps": ["Please try again later", "Consult with a local lawyer"],
                    "legal_references": [],
                }
