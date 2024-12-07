import requests

SERP_API_KEY = "fe4efb6db1358a7dc3fd47e974730722ff5cc2ec39721375833d2592e57e9a80"
query = "Tesla in Automotive"
url = f"https://serpapi.com/search.json?q={query}&api_key={SERP_API_KEY}"

response = requests.get(url)
print(response.json())