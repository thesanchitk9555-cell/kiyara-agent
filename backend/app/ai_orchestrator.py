import asyncio
import openai
import google.generativeai as genai
import httpx
from app.config import settings

class AIOrchestrator:
    def __init__(self):
        self.models = {
            "gemini": self._call_gemini,
            "openai": self._call_openai,
            "deepseek": self._call_deepseek
        }
        self.priority = ["gemini", "openai", "deepseek"]
        
        # Configure Gemini
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')
        except Exception as e:
            print(f"❌ Gemini init error: {e}")
            self.gemini_model = None
            
        # Configure OpenAI
        try:
            self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        except Exception as e:
            print(f"❌ OpenAI init error: {e}")
            self.openai_client = None

    async def generate(self, prompt: str, context: dict = None) -> str:
        full_prompt = f"""
        You are Kiyara, a warm, empathetic female voice assistant for Chandra Bhanu Gupt Agriculture College.
        Respond in natural, conversational Hindi/English mix.
        College details: established 1995, courses B.Sc(Ag), M.Sc, placements up to 6 LPA, hostel fees ₹18k, scholarships available.
        Be helpful, friendly, and concise.
        User asked: {prompt}
        """
        if context:
            full_prompt += f"\nContext: {context}"

        for name in self.priority:
            try:
                if name == "gemini" and self.gemini_model:
                    response = await self._call_gemini(full_prompt)
                elif name == "openai" and self.openai_client:
                    response = await self._call_openai(full_prompt)
                elif name == "deepseek":
                    response = await self._call_deepseek(full_prompt)
                else:
                    continue
                    
                if response:
                    return response
            except Exception as e:
                print(f"⚠️ {name} error: {e}")
                continue
                
        return "मैं अभी व्यस्त हूँ, कृपया थोड़ी देर बाद कॉल करें।"

    async def _call_gemini(self, prompt):
        if not self.gemini_model:
            raise Exception("Gemini not configured")
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(None, self.gemini_model.generate_content, prompt)
        return resp.text

    async def _call_openai(self, prompt):
        if not self.openai_client:
            raise Exception("OpenAI not configured")
        resp = await self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return resp.choices[0].message.content

    async def _call_deepseek(self, prompt):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}"},
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30.0
            )
            return resp.json()["choices"][0]["message"]["content"]