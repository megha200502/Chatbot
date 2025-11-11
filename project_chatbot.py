import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI


os.environ["GOOGLE_API_KEY"] ='API_key'

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
memory = ConversationBufferMemory()


chat = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  
)

print(" Gemini Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("You: ").strip()
    if not user_input:
        continue
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Bye!")
        break

    try:
        response = chat.run(user_input)
        print("AI:", response)
    except Exception as e:
        print("❌ Error:", e)
