import urllib.parse
import aiohttp  # Asynchronous HTTP requests
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.WARNING)

# Search query for Responsible AI ethics, societal, and philosophical impacts
search_query = "responsible AI ethics societal philosophical"
encoded_query = urllib.parse.quote(search_query)
base_url = 'http://export.arxiv.org/api/query?search_query=all:'
start_index = 0  # Starting index for fetching papers
max_results = 1  # Number of papers to fetch at a time

# Function to fetch paper details
async def eth_papers():
    global start_index
    try:
        url = f'{base_url}{encoded_query}&start={start_index}&max_results={max_results}'
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
                        
                        # Prepare the extracted information
                        paper_details = {
                            "title": paper_title,
                            "summary": paper_summary,
                            "authors": authors
                        }
                    else:
                        paper_details = None

                except ET.ParseError:
                    logging.error("Error parsing XML data", exc_info=True)
                    paper_details = None
           
           # Increment the start index to fetch the next paper in the next call
        start_index += 1
        return paper_details

    except aiohttp.ClientError:
        logging.error("Error fetching data", exc_info=True)
        return None
