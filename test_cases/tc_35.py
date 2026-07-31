# All secrets safely loaded from environment
import os
api_key = os.getenv("API_KEY")
db_password = os.getenv("DB_PASSWORD")
secret_key = os.getenv("SECRET_KEY")
