import cohere
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Hugging Face Inference API Key
HF_API_KEY = os.getenv('HF_HOME_TOKEN')

# Cohere API Key
COHERE_API_KEY = os.getenv('COHERE_API_KEY')

# SerpAPI Key for Web Search
SERP_API_KEY = os.getenv('SERP_API_KEY')

def fetch_huggingface_completion(prompt, model="tiiuae/falcon-7b-instruct"):
    """
    Generate text completions using Hugging Face Inference API.
    """
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 500, "temperature": 0.7}}
    url = f"https://api-inference.huggingface.co/models/{model}"

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return f"Error: {response.status_code} - {response.json()}"

def fetch_cohere_completion(prompt, model="command-xlarge-nightly"):
    """
    Generate text completions using Cohere API.
    """
    co = cohere.Client(COHERE_API_KEY)
    response = co.generate(model=model,
                           prompt=prompt,
                           max_tokens=2200
                           )
    return response.generations[0].text.strip()