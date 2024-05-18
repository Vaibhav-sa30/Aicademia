from uagents import Agent, Context
import urllib.parse
import aiohttp  # Asynchronous HTTP requests
import xml.etree.ElementTree as ET
import asyncio
import logging

# Configure logging to show only warnings and errors
logging.basicConfig(level=logging.WARNING)

ENGINEER = "Responsible AI Engineer Agent"
SEED_PHRASE = "Responsible AI Seed Phrase"

# More specific search query for Responsible AI
search_query = "transformers"
encoded_query = urllib.parse.quote(search_query)

print(f'We are searching for {encoded_query} query')

url = f'http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results=1'

engineer = Agent(name=ENGINEER, seed=SEED_PHRASE)

@engineer.on_interval(period=5)
async def fetch_paper(ctx: Context):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.text()
                
                try:
                    root = ET.fromstring(data)
                    entry = root.find('{http://www.w3.org/2005/Atom}entry')

                    if entry is not None:
                        # Extract title, summary, and author(s)
                        paper_title = entry.find('{http://www.w3.org/2005/Atom}title').text
                        paper_summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()  # Remove leading/trailing whitespace
                        authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
                        
                        # Print the extracted information
                        print(f"Title: {paper_title}")
                        print(f"Summary: {paper_summary}")
                        print(f"Authors: {', '.join(authors)}")
                    else:
                        print("No 'entry' element found in the response. Paper details unavailable.")
                except ET.ParseError:
                    logging.error("Error parsing XML data", exc_info=True)

    except aiohttp.ClientError:
        logging.error("Error fetching data", exc_info=True)

if __name__ == "__main__":
    asyncio.run(engineer.run())















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
