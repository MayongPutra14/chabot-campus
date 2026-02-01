import random
import yaml
import os
from sentence_transformers import SentenceTransformer, util
from chatbot.preprocess import clean_text
from chatbot.context import ContextManager


class ChatbotEngine:
    def __init__(self, dataset_path):
        self.dataset = self.load_knowledge_folder(dataset_path)
        self.context = ContextManager() # initialize Context Manager
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2") # load multy languages including indonesian language
        self.last_response_index = {}

        # Optimation: calculate embedding pattern in the first time.
        for intent in self.dataset:
            intent['pattern_embeddings'] = [
                self.model.encode(clean_text(p)) 
                for p in intent['patterns'] 
                ]

    
    def load_knowledge_folder(self, folder_path):
        intents = []

        for filename in os.listdir(folder_path):
            if not filename.endswith(".yml"):
                continue

            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            
            topic = data.get("topic")
            knowledge_list = data.get("knowledge", [])

            if not topic or not knowledge_list:
                continue # SKIP BROKEN FILE
            
            for item in knowledge_list:
                questions = item.get("questions", [])
                answer = item.get("answer")

                if not questions or not answer:
                    continue

                intents.append({
                    "tag": topic,
                    "patterns": questions,
                    "responses":answer
                }) 
        if not intents:
            raise ValueError("Knowledge folder kosong atau tidak valid")
        
        return intents
    
    def detect_intent(self, user_input):
        user_input = clean_text(user_input)
        user_embedding = self.model.encode(user_input)

        best_intent = None
        best_score = 0.0

        for intent in self.dataset:
            for pattern_embedding in intent["pattern_embeddings"]:
                score = util.cos_sim(user_embedding, pattern_embedding)[0][0]
                score = float(score)

                if score > best_score:
                    best_score = score
                    best_intent = intent
        return best_intent, best_score

    def pick_response(self, intent):
        responses = intent["responses"]
        tag = intent["tag"]

        if len(responses) == 1:
            return responses[0]

        last_index = self.last_response_index.get(tag)

        choices = list(range(len(responses)))
        if last_index in choices:
            choices.remove(last_index)

        new_index = random.choice(choices)
        self.last_response_index[tag] = new_index

        return responses[new_index]

    
    # Get chatbot response
    def get_response(self, user_input):
        intent, score = self.detect_intent(user_input)

        # Threshold Believe
        threshold = 0.55
        if intent and score >= threshold:
            self.context.update(intent["tag"])
            return self.pick_response(intent)

        # If chatbot confused, check lats context
        last_intent_tag = self.context.getLastIntent()
        if(last_intent_tag):
            for intent_data in self.dataset:
                if intent_data["tag"] == last_intent_tag:
                    return "Terkait hal itu, " + self.pick_response(intent_data)
                    
        return "Maaf, saya belum memahami pertanyaan itu. Bisa dijelaskan lebih detail?"
        