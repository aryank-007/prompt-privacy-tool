# Sample 07: Keyword argument passing credentials to a call
import requests

response = requests.post(
    "https://api.example.com/login",
    auth=("admin", "mysecret"),
    json={"password": "mysecret"},
)
