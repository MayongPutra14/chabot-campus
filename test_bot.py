import os
os.environ["HF_HOME"] = "./model_cache"
from chatbot.engine import ChatbotEngine

bot = ChatbotEngine("data/dataset_poltekintaz.yml")

while True:
    user = input("Anda: ")
    if user.lower() == "exit":
        break
    print("Bot:", bot.get_response(user))
