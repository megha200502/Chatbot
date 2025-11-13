import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader



os.environ["GOOGLE_API_KEY"] = "api_key"

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Memory
memory = ConversationBufferMemory()

# Chatbot
chat = ConversationChain(llm=llm, memory=memory, verbose=True)


# PDF Reader Function
def load_pdf_into_memory(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    pdf_text = "\n".join([p.page_content for p in pages])

    # Add PDF text to chatbot memory
    memory.chat_memory.add_user_message("PDF KNOWLEDGE: " + pdf_text)

    print("\n📄 PDF Loaded Successfully!")
    print("📌 Now the chatbot will answer using this PDF.\n")


print("Local PDF Knowledge Chatbot Ready!")
print("Commands:")
print(" readpdf <path>  → Load PDF")
print(" exit            → Quit\n")


# Main Loop
while True:
    user_input = input("You: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("👋 Bye!")
        break

    # Check PDF command
    if user_input.lower().startswith("readpdf "):
        path = user_input.replace("readpdf ", "").strip()
        load_pdf_into_memory(path)
        continue

    # Normal chat (PDF-based answers)
    response = chat.run(user_input)
    print("AI:", response)
