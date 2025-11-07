from transformers import pipeline, Conversation

# Model load (DialoGPT-medium का उदाहरण)
chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")

print("🤖 Chatbot Ready. Type 'exit' to quit.")

# Create a conversation object to keep context
conversation = Conversation()

while True:
    user_text = input("You: ")
    if user_text.strip().lower() in ["exit", "quit"]:
        print("Bot: Goodbye 👋")
        break

    conversation.add_user_input(user_text)
    chatbot(conversation)  # updates conversation.generated_responses
    reply = conversation.generated_responses[-1]
    print("Bot:", reply)
