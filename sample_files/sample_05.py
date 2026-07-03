# Sample 05: AWS credentials hardcoded
aws_access_key = "AKIAIOSFODNN7EXAMPLE"
aws_secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
region = "us-east-1"

import boto3
client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret,
)
