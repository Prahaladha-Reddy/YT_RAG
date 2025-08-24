class LLMClient:
    def __init__(self, **kwargs): ...
    def complete(self, prompt: str): raise NotImplementedError
    def chat(self, messages): raise NotImplementedError
