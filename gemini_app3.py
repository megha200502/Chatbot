import google.generativeai as genai
import os
import json

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
google_api_key = config_data["GOOGLE_API_KEY"]

# Configure Gemini
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

print("Enter 'exit' to stop the program")

while True:
    user_question = input("Enter your question: ")

    if user_question.lower() == "exit":
        print("Program stopped.")
        break

    prompts = [
        user_question,                                # Normal answer
        f"Answer briefly: {user_question}",           # Short answer
        f"Answer with a simple example: {user_question}"  # Example-style answer
    ]

    for i, prompt in enumerate(prompts, 1):
        response = model.generate_content(prompt)
        print(f"\n--------- Output {i} ---------")
        print(response.text)
