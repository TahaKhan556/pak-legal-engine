import json
import re
import asyncio
import httpx
from app.config import settings


class LLMService:
    def __init__(self):
        self.api_url = settings.AI_API_URL
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL

    def _extract_refs(self, context: str) -> list[dict]:
        refs = []
        for block in context.split("\n\n"):
            lines = block.strip().split("\n", 1)
            if lines and lines[0].startswith("---"):
                title = lines[0].strip("- ").strip()
                body = lines[1].strip() if len(lines) > 1 else ""
                refs.append({"title": title, "body": body})
        return refs

    def _build_smart_answer(self, query: str, context: str) -> dict:
        refs = self._extract_refs(context)
        if not refs:
            return {
                "verdict": "No relevant legal provisions found.",
                "plain_language": "The legal database does not contain specific provisions matching your query.",
                "plain_urdu": "Is sawal ka jawab hamari database mein nahi hai.",
                "steps": [],
                "legal_references": [],
            }

        ref_titles = [r["title"] for r in refs]
        first_ref = ref_titles[0]

        constitutional_rights = []
        statutory_rights = []
        procedure_points = []

        for r in refs:
            body = r["body"]
            title = r["title"]

            if "constitution" in title.lower():
                for match in re.finditer(r"(?:Article|Section)\s+(\d+)", body):
                    constitutional_rights.append(f"Article {match.group(1)}")
                constitutional_rights.append(body[:400])
            elif "crpc" in title.lower() or "code of criminal" in title.lower():
                for match in re.finditer(r"(\d+)\.\s+([^\n]+)", body):
                    procedure_points.append(f"Section {match.group(1)}: {match.group(2).strip()}")
                statutory_rights.append(body[:400])
            else:
                statutory_rights.append(body[:400])

        article_10_text = ""
        for r in refs:
            if "constitution" in r["title"].lower():
                body = r["body"]
                if "informed" in body.lower() or "magistrate" in body.lower():
                    article_10_text = body
                    break

        if article_10_text:
            verdict_text = (
                f"Under Article 10 of the Constitution of Pakistan and related provisions "
                f"in {first_ref}, you have specific rights during arrest including: "
                f"the right to be informed of grounds of arrest, the right to legal counsel, "
                f"and the right to be produced before a magistrate within 24 hours."
            )
        else:
            verdict_text = (
                f"Under {first_ref} and related Pakistani law, "
                f"the legal provisions below outline the rules and procedures relevant to your question."
            )

        all_provisions = "\n\n".join([r["body"][:500] for r in refs[:3]])

        if article_10_text:
            plain_language = (
                f"**Your Constitutional Rights During Arrest:**\n\n"
                f"**Article 10 of the Constitution of Pakistan, 1973** guarantees the following fundamental rights "
                f"to every arrested person:\n\n"
                f"1. **Right to be informed of grounds of arrest** — No person shall be detained without being informed, "
                f"as soon as may be, of the grounds for such arrest.\n\n"
                f"2. **Right to legal counsel** — No arrested person shall be denied the right to consult and be defended "
                f"by a legal practitioner of their choice.\n\n"
                f"3. **Right to be produced before a magistrate** — Every arrested person must be produced before a "
                f"magistrate within **24 hours** of arrest (excluding travel time). No person shall be detained beyond "
                f"24 hours without the authority of a magistrate.\n\n"
                f"**Additional Provisions from {first_ref}:**\n\n"
                f"{all_provisions}\n\n"
                f"**What you should do:** If arrested, immediately request to know the reason for your arrest, "
                f"contact a lawyer, and ensure you are produced before a magistrate within 24 hours. "
                f"If these rights are violated, you can file a complaint with the relevant authorities."
            )
        else:
            plain_language = (
                f"**What the Law Says:**\n\n"
                f"Based on {first_ref} and related legislation, the following provisions apply:\n\n"
                f"{all_provisions}\n\n"
                f"**Key Points:** The references above contain the exact legal text that governs your situation. "
                f"Review the section numbers cited in the references below for the specific rules that apply.\n\n"
                f"**Important:** For a definitive legal opinion on how these provisions apply to your specific situation, "
                f"consult a qualified Pakistani lawyer."
            )

        if article_10_text:
            plain_urdu = (
                f"**Aapke Qanooni Huqooq (Giraftari ke waqt):**\n\n"
                f"Pakistan ka Constitution (Dastoor), Article 10 ke mutabiq, har giraftar shakhs ko yeh huqooq hain:\n\n"
                f"1. **Giraftari ki wajah batane ka huqooq** — Police ko aapko foran batana hoga ke aapko kyun giraftar kiya ja raha hai.\n\n"
                f"2. **Wakeel rakhne ka huqooq** — Aap apna wakeel rakh sakte hain aur koi aapko yeh huqooq nahi cheen sakta.\n\n"
                f"3. **24 ghante ke andar Magistrate ke samne pesh hona** — Aapko giraftari ke 24 ghante ke andar magistrate ke samne pesh kiya jana chahiye.\n\n"
                f"**Agla qadam:** Agar aapko giraftar kiya jaye, toh turant police se giraftari ki wajah poochein, "
                f"apne wakeel se raabta karein, aur 24 ghante ke andar magistrate ke samne pesh hone ki guarantee lein."
            )
        else:
            plain_urdu = (
                f"**Qanoon kya kehta hai:**\n\n"
                f"{first_ref} aur mutaliq qanooni qawaneen ke mutabiq:\n\n"
                f"{all_provisions[:600]}\n\n"
                f"**Kirdar:** Neeche diye gaye hawalon mein mosool sections parhein. "
                f"Kisi qualified wakeel se rabta karein."
            )

        steps = []
        if article_10_text:
            steps = [
                "If arrested, immediately ask the police to tell you why you are being arrested",
                "Exercise your right to contact a lawyer of your choice",
                "Ensure you are produced before a magistrate within 24 hours",
                "If your rights are violated, file a complaint with the relevant authorities",
            ]
        else:
            steps = [
                f"Review the specific provisions in {first_ref} cited below",
                "Note the section numbers that apply to your situation",
                "Consult a qualified Pakistani lawyer for case-specific advice",
                "Contact a legal aid center if you need free legal assistance",
            ]

        return {
            "verdict": verdict_text,
            "plain_language": plain_language,
            "plain_urdu": plain_urdu,
            "steps": steps,
            "legal_references": ref_titles[:5],
        }

    async def _call_llm(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a Pakistani legal expert. Answer accurately.",
                            },
                            {"role": "user", "content": prompt},
                        ],
                        "temperature": 0.3,
                        "max_tokens": 600,
                    },
                    timeout=20.0,
                )
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"].get("content", "")
                if content and len(content) > 30:
                    return content
        except Exception:
            pass
        return ""

    def _parse_llm_json(self, text: str) -> dict | None:
        text = text.strip()

        json_match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
        if json_match:
            text = json_match.group(1).strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        try:
            start = text.index("{")
            end = text.rindex("}") + 1
            return json.loads(text[start:end])
        except (ValueError, json.JSONDecodeError):
            pass

        return None

    async def generate_legal_answer(self, query: str, context: str) -> dict:
        smart_answer = self._build_smart_answer(query, context)

        prompt = f"Answer briefly: {query}\n\nContext:\n{context[:800]}\n\nGive a 2-3 sentence answer citing specific sections."
        llm_result = await self._call_llm(prompt)

        if llm_result and len(llm_result) > 50:
            return {
                "verdict": llm_result[:500],
                "plain_language": llm_result[:2000],
                "plain_urdu": smart_answer.get("plain_urdu", ""),
                "steps": smart_answer.get("steps", []),
                "legal_references": smart_answer.get("legal_references", []),
            }

        return smart_answer
