# Sample 10: Mixed — some sensitive, some not
import os

PORT = 8080
HOST = "localhost"
DEBUG = True

# Loaded safely from environment
private_key = os.getenv("PRIVATE_KEY")
auth_token = os.environ.get("AUTH_TOKEN", "")

def handle_request(user_id, password):
    data = {"user": user_id, "credentials": password}
    return data
