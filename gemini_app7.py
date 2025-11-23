from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import google.generativeai as genai
import json
import os

app = FastAPI()

# Load API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config = json.load(open(f"{working_dir}/config.json"))
genai.configure(api_key=config["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-flash")

async def stream_model(prompt):
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        if chunk.text:
            yield chunk.text
            await asyncio.sleep(0.01)

@app.post("/stream")
async def stream_api(data: dict):
    prompt = data.get("prompt", "")
    return StreamingResponse(stream_model(prompt), media_type="text/plain")
