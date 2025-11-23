import os
import json
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# Load API Key From config.json
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
google_api_key = config_data["GOOGLE_API_KEY"]

# Configure Gemini
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# FastAPI App
app = FastAPI()

class UserInput(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_text(data: UserInput):
    response = model.generate_content(data.prompt)
    return {"response": response.text}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
