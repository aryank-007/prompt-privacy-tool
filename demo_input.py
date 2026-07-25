# Developer's config file — about to be pasted into an AI assistant for debugging
import boto3
import requests

aws_access_key = "AKIAIOSFODNN7ABCDEFG"
aws_secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYABCDEFGHIJ"
api_key = "sk_live_51Hh7Y2KZ3AbCdEfGhIjKlMnOpQrStUvWx"
db_password = "Tr0ub4dor&3SecurePass99"

def upload_file(filename):
    client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret,
    )
    client.upload_file(filename, "my-bucket", filename)

def send_notification(message):
    requests.post(
        "https://api.example.com/notify",
        headers={"Authorization": "Bearer " + api_key},
        json={"text": message},
    )
