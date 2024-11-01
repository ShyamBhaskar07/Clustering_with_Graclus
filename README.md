# Text Data Collection and Graph Clustering Project

This project is designed to collect text data from PubMed articles, structure it as a graph for clustering, and identify the top 20 words from each cluster. The project consists of three primary scripts: `extract.py`, `graph.py`, and `top20.py`.

## Project Structure
- **extract.py**: Collects text data from PubMed URLs and saves it to the `data` folder.
- **graph.py**: Processes the collected text data to create an adjacency list, a vocabulary file, and an initial graph (`input.graph`).
- **graclus**: Clusters the graph into a specified number of clusters (e.g., 200).
- **top20.py**: Analyzes each cluster to extract the top 20 words from the vocabulary and saves them in `top_20_words.txt`.

## Files and Output
- **pubmed_urls.txt**: A list of PubMed URLs to scrape.
- **data folder**: Stores raw text data collected from each URL.
- **input.graph**: Graph file generated from `graph.py` that represents relationships between text entities.
- **input.graph.part.200**: Output of Graclus clustering, containing clusters (e.g., 200 clusters).
- **vocabulary.txt**: List of unique words collected from the text data.
- **top_20_words.txt**: List of the top 20 words for each cluster.

## Dependencies
- `BeautifulSoup`: For parsing HTML content.
- `Graclus` clustering software: Ensure it’s installed and accessible in your system's PATH.
