# Sample 09: Multiple secrets spread across a class
class AppConfig:
    def __init__(self):
        self.db_password = "P@ssw0rd!"
        self.api_key = "live_key_abc987"
        self.client_secret = "cs_test_XYZ"
        self.app_name = "MyApp"
        self.version = "1.0.0"
