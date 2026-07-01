from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Gemini API Key મેળવો (Railway પરથી લોડ થશે)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6Klk676bPTco9ceeZnFZw4D-5ALkPJS7Pvkq35N-KHmPQ")
genai.configure(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str

# AI ને ટ્રેન કરવા માટેની મહત્વની ઇન્સ્ટ્રક્શન
SYSTEM_INSTRUCTION = """
You are an expert AI Assistant for Lubi Electronics (www.lubielectronics.com). 
Your job is to assist customers with their queries regarding industrial automation, 
solar products, embedded systems, and general electrical components. 
Be professional, polite, and directly helpful. If you don't know the answer about a specific 
product, ask them to contact support@lubielectronics.com. Respond in Gujarati or English based on user's input.
"""

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_INSTRUCTION
        )
        response = model.generate_content(request.message)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()