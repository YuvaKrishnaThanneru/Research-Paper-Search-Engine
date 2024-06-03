import time  # Module for time-related operations
import ujson  # Module for working with JSON data
from random import randint  # Module for generating random numbers
from typing import Dict, List, Any  # Type hinting imports

import requests  # Library for making HTTP requests

def write_papers(list1, file_name):
    # Function to write papers' URLs to a file
    with open(file_name, 'w', encoding='utf-8') as f:
        for i in range(0, len(list1)):
            f.write(list1[i] + '\n')


def initCrawlerScraper(seed, max_papers=500):
    # Initialize parameters for the arXiv API
    base_url = "http://export.arxiv.org/api/query?"  # Base URL for the API
    search_query = "all:information+retrieval"  # Search query for the papers
    start = 0  # Start index for the results
    max_results = 100  # Maximum number of results per request
    wait_time = 3  # Wait time between requests in seconds
    headers = {"User-Agent": "arXivCrawlerScraper"}  # User agent for the requests

    Links = []  # Array with arXiv papers URL
    pub_data = []  # To store publication information for each arXiv paper

    print("Crawler has begun...")
    while (start < max_papers):
        # Construct the query URL
        query = f"{base_url}search_query={search_query}&start={start}&max_results={max_results}"
        # Make a GET request to the API
        response = requests.get(query, headers=headers)
        # Check the status code of the response
        if response.status_code == 200:
            # Parse the response as XML
            response_xml = response.text
            # Find all the entries in the XML
            entries = response_xml.split("<entry>")
            # Loop through the entries
            for entry in entries[1:]:
                # Extract the paper URL
                paper_url = entry.split("<id>")[1].split("</id>")[0]
                # Append the paper URL to the Links array
                Links.append(paper_url)
                # Extract the publication data as JSON
                paper_data = {
                    "name": entry.split("<title>")[1].split("</title>")[0],
                    "cu_author": ",".join([author.split("<name>")[1].split("</name>")[0] for author in entry.split("<author>")[1:]]),
                    
                    "date": entry.split("<published>")[1].split("</published>")[0],
                    
                    "pub_url": entry.split("<id>")[1].split("</id>")[0]
                    }
                # Append the paper data to the pub_data array
                pub_data.append(paper_data)
            # Increment the start index by the max_results
            start += max_results
            # Wait for some time before making the next request
            time.sleep(wait_time)
        else:
            # Handle the error
            print(f"Error: {response.status_code}")
            break
    # Write the papers' URLs to a file
    write_papers(Links, "arxiv_papers.txt")
    # Return the publication data
    return pub_data


# Start the crawler and scraper with the seed URL
seed = "http://export.arxiv.org/api/query?search_query=all:information+retrieval&start=0&max_results=1"
pub_data = initCrawlerScraper(seed)

# Convert the pub_data array into a JSON string
pub_data_json = ujson.dumps(pub_data)
# Open a file named "arxiv_papers.json" in write mode
with open("arxiv_papers.json", "w", encoding="utf-8") as f:
    # Write the JSON string to the file
    f.write(pub_data_json)
