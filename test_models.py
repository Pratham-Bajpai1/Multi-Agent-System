from utils import fetch_cohere_completion

# Testing Cohere's ability to generate 10 detailed use cases in the desired structure

# Define a sample prompt based on the provided structure
test_prompt = """
Generate 10 detailed AI/ML use cases for the industry 'Steel Manufacturing'. 
Each use case must follow this format:

Title: [A short and descriptive title]
Objective/Use Case: [A high-level goal of the use case]
AI Application: [A detailed explanation of how AI/ML is applied to achieve the objective]
Cross-Functional Benefits:
- Operations: [Operational benefits]
- Finance: [Financial benefits]
- Quality Assurance: [Quality-related benefits]

Ensure each use case is clear, concise, and detailed. Separate each use case with the delimiter '---'.
"""

# Fetch the response from Cohere with a high token limit
response = fetch_cohere_completion(
    prompt=test_prompt,
    model="command-xlarge-nightly",
)

# Print the raw response for analysis
response.strip()
print(response)
