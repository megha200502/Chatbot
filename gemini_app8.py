#  WARNINGS FIX 
import warnings
warnings.filterwarnings("ignore")

import os
import json
import numexpr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import AgentExecutor, create_react_agent, Tool

# New Import (hub nahi, LangSmith)
from langsmith import Client

# 2. Configuration
working_dir = os.path.dirname(os.path.abspath(__file__))
try:
    config_data = json.load(open(f"{working_dir}/config.json"))
    google_api_key = config_data["GOOGLE_API_KEY"]
except FileNotFoundError:
    print("Error: config.json file not found!")
    exit()

# 3. LLM Setup (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key,
    temperature=0
)

# 4. Tools Setup
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

def safe_calc_tool(query: str):
    try:
        return str(numexpr.evaluate(query.strip()))
    except:
        return "Calculation Error"

tools = [
    Tool(name="Search", func=wiki.run,
         description="Search facts using Wikipedia"),
    Tool(name="Calculator", func=safe_calc_tool,
         description="Math operations using numexpr")
]

# 5. Create Agent — hub.pull() HATA DIYA  


client = Client()
prompt = client.pull_prompt("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# 6. Run
if __name__ == "__main__":
    print("\nCalculator")
    print("What is the population of India divided by 2?")

    while True:
        q = input("\nEnter query (or 'exit'): ")
        if q.lower() in ["exit", "quit"]:
            break

        try:
            resp = agent_executor.invoke({"input": q})
            print(f"\n Final Answer: {resp['output']}")
        except Exception as e:
            print(f"Error: {e}")
