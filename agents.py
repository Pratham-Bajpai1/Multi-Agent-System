import requests
from utils import fetch_huggingface_completion, fetch_cohere_completion
import json
import re


class ResearchAgent:
    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query):
        url = f"https://serpapi.com/search.json?q={query}&api_key={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            # Extract relevant information
            results = response.json().get("organic_results", [])
            return [
                {
                    "Key Findings": res.get("snippet", "No snippet available"),
                    "Source Link": res.get("link", "No link available")
                }
                for res in results
            ]
        return [{"Key Findings": f"Error: {response.status_code} - {response.text}", "Source Link": "N/A"}]


class UseCaseGenerator:
    def __init__(self, llm_provider="cohere"):
        self.llm_provider = llm_provider

    def generate(self, input_data, company):
        prompt = f"""
        Generate 10 innovative AI/ML use cases tailored to the company '{company}' in the industry '{input_data}'.
        Each use case must align with the company's strategic goals and industry challenges, focusing on innovation and operational improvements.
        Ensure each use case follows this exact format:

        Title: [A short and descriptive title]
        Description: [A detailed explanation of how this AI/ML solution can be applied, emphasizing innovation and strategic impact.]
        Benefits: [A list of exactly 3 distinct benefits focusing on innovation, efficiency, and long-term impact.]

        Separate each use case with the delimiter `---`.

        Example:
        Title: Predictive Maintenance
        Description: AI predicts maintenance needs using sensor data, reducing unexpected breakdowns and improving fleet reliability. By analyzing sensor readings and maintenance history, ML models identify patterns and recommend proactive actions.
        Benefits: [Reduced Downtime, Cost Savings, Improved Safety]

        Ensure the response adheres to this structure and highlights innovative, impactful, and relevant applications.
        """

        if self.llm_provider == "cohere":
            response = fetch_cohere_completion(prompt)
        else:
            raise ValueError("Invalid LLM provider specified.")

        # Debug: Print raw response
        print("RAW RESPONSE:", response)

        # Split the response into individual use cases
        use_cases_raw = response.split("---")
        use_cases = []

        for use_case_raw in use_cases_raw:
            lines = use_case_raw.strip().split("\n")
            title = ""
            description = ""
            benefits = []

            for line in lines:
                if line.startswith("Title:"):
                    title = line.split("Title:", 1)[1].strip()
                elif line.startswith("Description:"):
                    description = line.split("Description:", 1)[1].strip()
                elif line.startswith("Benefits:"):
                    benefits_line = line.split("Benefits:", 1)[1].strip()
                    # Split benefits using regex to detect numbers followed by a period
                    benefits = re.split(r"\d\.\s", benefits_line)
                    # Clean up any empty strings or whitespace in the list
                    benefits = [b.strip("[] ").strip() for b in benefits if b.strip()]

            if title and description and benefits:
                use_cases.append({
                    "Use Case": title,
                    "Description": description,
                    "Benefits": benefits
                })

        # Debug: Print parsed use cases
        print("Parsed Use Cases:", use_cases)

        return use_cases

class DatasetCollector:
    def collect(self, keyword):
        kaggle_url = f"https://www.kaggle.com/search?q={keyword}"
        huggingface_url = f"https://huggingface.co/models?search={keyword}"
        return [
            {"Platform": "Kaggle", "URL": kaggle_url},
            {"Platform": "HuggingFace", "URL": huggingface_url},
        ]
