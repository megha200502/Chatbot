import os
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import json

# -------------------------
# Logging Setup
# -------------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------
# Load API Key From config.json
# -------------------------
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
google_api_key = config_data.get("GOOGLE_API_KEY")

if not google_api_key:
    raise Exception("API Key not found in config.json")

# Configure Gemini
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI()

class UserInput(BaseModel):
    prompt: str


@app.post("/generate")
async def generate_text(data: UserInput):
    try:
        logging.info(f"Prompt received: {data.prompt}")

        response = model.generate_content(data.prompt)

        if not response or not response.text:
            logging.error("Empty model response")
            raise HTTPException(
                status_code=500,
                detail="Model returned empty response"
            )

        logging.info("Response generated successfully")
        return {"response": response.text}

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the response"
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
