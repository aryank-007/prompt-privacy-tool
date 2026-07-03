# Sample 03: Reading secrets from environment variables
import os

db_url = os.getenv("DATABASE_URL")
secret_key = os.environ["SECRET_KEY"]
debug = os.getenv("DEBUG", "false")
