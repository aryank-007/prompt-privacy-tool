# Secret stored as a class attribute — tool misses self.x = ... assignments
class Config:
    def __init__(self):
        self.api_key = "sk_live_AbCdEfGhIjKlMnOpQrStUvWx"
