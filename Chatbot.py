import chatterbot as cb

chatbot = cb("Angela")

conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]
trainer = ListTrainer(chatbot)

response = chatbot.get_response("Good morning!")
print(response)