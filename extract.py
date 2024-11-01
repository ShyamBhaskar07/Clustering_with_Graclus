import os
import requests
from bs4 import BeautifulSoup

# Directory setup for saving abstracts
abstracts_dir = 'data/'  # Update this to the desired output directory
os.makedirs(abstracts_dir, exist_ok=True)

# File containing the URLs
url_file_path = 'pubmed_urls.txt'  # Update this to the correct path

# Function to extract the abstract from the specified URL
def extract_abstract(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract the abstract within the specified div
            abstract_div = soup.find('div', class_='abstract-content selected', id='eng-abstract')
            if abstract_div:
                # Get the text inside the paragraph tags and strip any extra spaces
                abstract_text = abstract_div.get_text(strip=True, separator=' ')
                return abstract_text
        # Return None if abstract not found or response is not 200
        return None
    except Exception as e:
        return None

# Read URLs from the input file
with open(url_file_path, 'r') as file:
    urls = [line.strip() for line in file.readlines()]

# Extract abstracts and save each to a separate file named d1.txt, d2.txt, etc.
file_index = 1
for url in urls:
    abstract = extract_abstract(url)
    if abstract:  # Skip if abstract is None
        file_name = f"d{file_index}.txt"
        file_path = os.path.join(abstracts_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as abstract_file:
            abstract_file.write(abstract)
        file_index += 1  # Increment the file index only if the abstract was saved

print(f"Abstracts have been saved in the directory: {abstracts_dir}")
