from uagents import Agent, Context
import urllib, urllib.request
import requests  # Library for making API requests

ENGINEER = "Responsible AI Engineer Agent"
SEED_PHRASE = "Responsible AI Seed Phrase"

# More specific search query for Responsible AI
search_query = "transformers"
encoded_query = urllib.parse.quote(search_query)

print(encoded_query)

url = f'http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results=2'

engineer = Agent(name=ENGINEER, seed=SEED_PHRASE)

data = urllib.request.urlopen(url)
print(data.read().decode('utf-8'))




'''
# Retry logic with a short delay (adjust as needed)
max_retries = 3
for attempt in range(1, max_retries + 1):
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for unsuccessful responses (200+)
    data = response.json()

    # Extract relevant information from the data (e.g., first paper's title)
    if data['totalResults'] > 0:
        first_paper_title = data['entries'][0]['title']
        print(f"Found paper: {first_paper_title}")
        break  # Exit the loop on successful retrieval
    else:
        print("No papers found matching the search criteria.")
        break  # Exit the loop on no results

  except requests.exceptions.RequestException as e:
    print(f"An error occurred during the API request (attempt {attempt}/{max_retries}): {e}")
    if attempt == max_retries:
        print("Maximum retries reached. Giving up.")


'''
