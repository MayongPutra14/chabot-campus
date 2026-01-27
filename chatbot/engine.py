import random
import yaml
from sentence_transformers import SentenceTransformer, util
from chatbot.preprocess import clean_text
from chatbot.context import ContextManager


class ChatbotEngine:
    def __init__(self, dataset_path):
        self.dataset = self.load_dataset(dataset_path) # load datase from data/
        self.context = ContextManager() # initialize Context Manager
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2") # load multy languages including indonesian language

        # Optimation: calculate embedding pattern in the first time.
        for intent in self.dataset:
            intent['pattern_embeddings'] = [self.model.encode(clean_text(p)) for p in intent['patterns'] ]


    def load_dataset(self,path):
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        # handler if dataset broke.
        for intent in data["intents"]:
            if "tag" not in intent or "patterns" not in intent or "responses" not in intent:
                raise ValueError("Dataset tidak valid! Setiap intent harus punya tag, patterns, dan responses")
        return data["intents"]
    
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
    
    # Get chatbot response
    def get_response(self, user_input):
        intent, score = self.detect_intent(user_input)

        # Threshold Believe
        threshold = 0.55
        if intent and score >= threshold:
            self.context.update(intent["tag"])
            return random.choice(intent["responses"])

        # If chatbot confused, check lats context
        last_intent_tag = self.context.getLastIntent()
        if(last_intent_tag):
            for intent_data in self.dataset:
                if intent_data["tag"] == last_intent_tag:
                    return "Terkait hal itu, " + random.choice(intent_data["responses"])
                    
        return "Maaf, saya belum memahami pertanyaan itu. Bisa dijelaskan lebih detail?"
        