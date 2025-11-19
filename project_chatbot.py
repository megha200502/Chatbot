from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader

# ----------------- AGENT IMPORTS -----------------
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
# --------------------------------------------------

app = FastAPI()

os.environ["GOOGLE_API_KEY"] = "api_key"  # Add your Gemini API Key

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

class ChatRequest(BaseModel):
    pdf_path: str | None = None
    query: str | None = None

# MEMORY
chat_history = ""


# ----------------- TOOLS -----------------
def calculator_tool(query: str):
    try:
        return str(eval(query))
    except:
        return "Invalid math expression."

calculator = Tool(
    name="Calculator",
    func=calculator_tool,
    description="Useful for solving math expressions."
)

def search_tool(query: str):
    return f"Search result for '{query}': Example data found!"

search_api = Tool(
    name="SearchAPI",
    func=search_tool,
    description="Useful for searching general information."
)

# Build the Agent
agent = initialize_agent(
    tools=[calculator, search_api],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False
)


# ---------------- STREAMING FUNCTION ----------------
async def stream_text(text):
    for word in text.split():
        yield word + " "
        await asyncio.sleep(0.02)



# ---------------- MAIN API ----------------
@app.post("/pdf_chat")
async def pdf_chat(req: ChatRequest):
    global chat_history

    pdf_path = req.pdf_path
    query = req.query

    # ----- PDF Load -----
    if pdf_path:
        if not pdf_path.lower().endswith(".pdf"):
            return {"error": "Invalid file format. Only .pdf allowed."}

        if not os.path.exists(pdf_path):
            return {"error": "PDF not found"}

        try:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
        except:
            return {"error": "Unable to read PDF"}

        chat_history = ""
        pdf_text = "\n".join([p.page_content for p in pages])
        chat_history += f"PDF DATA:\n{pdf_text}\n"

        if not query:
            return {"message": "PDF loaded successfully"}


    # ----- Query Missing -----
    if not query:
        return {"error": "Please enter a question"}


    # Build prompt
    prompt = chat_history + f"\nUser: {query}\nAssistant:"


    # ---------------- SMART AGENT + CHATGPT FALLBACK ----------------
    try:
        # Try agent first (PDF + Tools)
        answer = await asyncio.to_thread(agent.run, prompt)

        # If agent gives blank/weak answer → fallback to normal chatbot
        if (answer is None 
            or answer.strip() == "" 
            or "sorry" in answer.lower() 
            or "could not" in answer.lower()):
            answer = await llm.apredict(query)

    except Exception:
        # If agent fails → normal chatbot answers
        answer = await llm.apredict(query)
    # -----------------------------------------------------------------


    # Save conversation history
    chat_history += f"\nUser: {query}\nAssistant: {answer}\n"

    # Stream final answer
    return StreamingResponse(stream_text(answer), media_type="text/plain")
