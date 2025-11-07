def chatbot():
    print("Chatbot: Hi! I am your chatbot ")
    
    while True:
        user = input("You:")
       
        
        if user.lower() in ["bye", "exit"]:
            print("Chatbot: Bye! Have a nice day ")
        
        elif user.lower() in ["hii", "exit"]:
            print("Chatbot: hello! ")
        
        elif user.lower() in ["how are you ?", "exit"]:
            print("Chatbot: i am fine, thank you ! ")
        
        elif user.lower() in [".", "exit"]:
            print("Chatbot: over ")
            break
        else:
            print("Chatbot: You said '" + user + "'")
chatbot()
