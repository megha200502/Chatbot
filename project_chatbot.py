from google import genai

api_key = 'api_key here'
client = genai.Client(api_key=api_key)
while True:
    user_input = input("Enter your message: ")

    
    if user_input.lower() in ["bye", "byy"]:
        print("byy")
        break  

    chat = client.chats.create(model="gemini-2.5-flash")
    response = chat.send_message(user_input)

    for message in chat.get_history()[-1:]:
        print(message.parts[0].text)
