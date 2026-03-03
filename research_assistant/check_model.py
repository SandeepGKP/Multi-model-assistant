import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ✅ Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ✅ List available models
models = client.models.list()

for model in models.data:
    print(model.id)