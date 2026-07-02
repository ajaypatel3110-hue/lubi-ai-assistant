from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Gemini API Key સેટઅપ
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6Klk676bPTco9ceeZnFZw4D-5ALkPJS7Pvkq35N-KHmPQ")
genai.configure(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str

# AI માટેની કસ્ટમ ટ્રેનિંગ ઇન્સ્ટ્રક્શન
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
        # અહીં આપણે સાદું મોડલ ઇનિશિયલાઇઝ કર્યું
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        # પ્રોમ્પ્ટની સાથે જ ઇન્સ્ટ્રક્શન જોડી દીધી જેથી જૂના વર્ઝનમાં પણ એરર ન આવે
        full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser Question: {request.message}"
        
        response = model.generate_content(full_prompt)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
