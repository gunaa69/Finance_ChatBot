# assistant.py
import os
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any

# HuggingFace fallback
from transformers import pipeline

# IBM Watson SDK
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

load_dotenv()

# Load env
WATSON_API_KEY = os.getenv("WATSON_API_KEY")
WATSON_URL = os.getenv("WATSON_URL")
WATSON_ASSISTANT_ID = os.getenv("WATSON_ASSISTANT_ID")

GRANITE_API_URL = os.getenv("GRANITE_API_URL")
GRANITE_API_KEY = os.getenv("GRANITE_API_KEY")

HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize HuggingFace QA pipeline as fallback/generic
try:
    hf_qa = pipeline("question-answering", model="deepset/roberta-base-squad2", device=-1)
except Exception as e:
    hf_qa = None
    print("HuggingFace pipeline init failed:", e)

# IBM Watson Assistant client helper
class WatsonAssistantClient:
    def __init__(self, api_key: str, url: str, assistant_id: str):
        if not api_key or not url or not assistant_id:
            self.client = None
            return
        authenticator = IAMAuthenticator(api_key)
        self.client = AssistantV2(version="2021-06-14", authenticator=authenticator)
        self.client.set_service_url(url)
        self.assistant_id = assistant_id

    def create_session(self) -> Optional[str]:
        if not self.client:
            return None
        resp = self.client.create_session(assistant_id=self.assistant_id).get_result()
        return resp.get("session_id")

    def message(self, session_id: str, text: str) -> str:
        if not self.client:
            return ""
        response = self.client.message(assistant_id=self.assistant_id, session_id=session_id,
                                       input={"message_type": "text", "text": text}).get_result()
        # extract text from response (may vary by assistant configuration)
        out_text = ""
        try:
            if "output" in response and "generic" in response["output"]:
                for g in response["output"]["generic"]:
                    if g.get("text"):
                        out_text += g["text"] + "\n"
        except Exception:
            pass
        return out_text.strip()

# Granite client (generic HTTP wrapper)
class GraniteClient:
    def __init__(self, api_url: Optional[str], api_key: Optional[str]):
        self.api_url = api_url
        self.api_key = api_key

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        if not self.api_url or not self.api_key:
            return ""
        payload = {
            "prompt": prompt,
            "max_tokens": max_tokens,
            # add other Granite-specific params as needed
        }
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        try:
            r = requests.post(self.api_url, json=payload, headers=headers, timeout=20)
            r.raise_for_status()
            j = r.json()
            # Expecting JSON like {"text": "..."} or {"choices":[{"text":"..."}]}
            if "text" in j:
                return j["text"]
            if "choices" in j and len(j["choices"]) > 0 and "text" in j["choices"][0]:
                return j["choices"][0]["text"]
            # fallback to raw string
            return str(j)
        except Exception as e:
            # return empty to let fallback handle it
            print("Granite request failed:", e)
            return ""


class AIOrchestrator:
    def __init__(self):
        self.watson = WatsonAssistantClient(WATSON_API_KEY, WATSON_URL, WATSON_ASSISTANT_ID)
        self.granite = GraniteClient(GRANITE_API_URL, GRANITE_API_KEY)
        
        self.watson_session = None
        if self.watson.client:
            try:
                self.watson_session = self.watson.create_session()
            except Exception as e:
                print("Watson session creation failed:", e)

    def ask(self, user_text: str, context: Optional[str] = None) -> Dict[str, Any]:
        """
        Returns a dict: {'source': 'watson'|'granite'|'hf', 'text': '...'}
        """
      
        if self.watson.client and self.watson_session:
            try:
                res = self.watson.message(self.watson_session, user_text)
                if res and res.strip():
                    return {"source": "watson", "text": res.strip()}
            except Exception as e:
                print("Watson message failed:", e)

        
        if self.granite.api_url and self.granite.api_key:
            try:
                prompt = user_text if not context else f"{context}\n\nUser: {user_text}"
                gen = self.granite.generate(prompt)
                if gen and gen.strip():
                    return {"source": "granite", "text": gen.strip()}
            except Exception as e:
                print("Granite failure:", e)

        
        if hf_qa:
            try:
                context = context or ("Savings are funds set aside; investments like mutual funds, ETFs, SIPs; "
                                     "tax-saving strategies include HRA, 80C investments, etc.")
                resp = hf_qa({"question": user_text, "context": context})
                answer = resp.get("answer", "")
                if answer:
                    return {"source": "hf", "text": answer}
            except Exception as e:
                print("HF QA failed:", e)

        # Last fallback — simple canned reply
        return {"source": "fallback", "text": "Sorry, I couldn't generate an answer right now. Try rephrasing."}
