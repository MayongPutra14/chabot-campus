class ContextManager:
    def __init__(self):
        self.last_intent = None

    def update(self, intent):
        self.last_intent = intent
        
    def getLastIntent(self):
        return self.last_intent
        
    def clear(self):
        self.last_intent = None