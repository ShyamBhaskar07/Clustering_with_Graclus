import os
import re
import nltk
from collections import defaultdict
import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from itertools import combinations

# Download stopwords if not already available
nltk.download('stopwords')
from nltk.corpus import stopwords

# Initialize stop words
stop_words = set(stopwords.words('english'))

# Function to preprocess text and remove stop words
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)  # Remove punctuation
    text = text.lower()  # Lowercase text
    words = text.split()  # Split text into words
    words = [word for word in words if word not in stop_words]  # Remove stop words
    return words

# Function to read and preprocess documents
def load_and_preprocess_documents(doc_dir):
    documents = []
    for filename in sorted(os.listdir(doc_dir)):
        if filename.endswith('.txt'):
            with open(os.path.join(doc_dir, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                documents.append(preprocess_text(text))
    return documents

# Function to build co-occurrence matrix
def build_cooccurrence_matrix(documents, vocabulary):
    vocab_index = {word: idx for idx, word in enumerate(vocabulary)}
    cooccurrence_matrix = np.zeros((len(vocabulary), len(vocabulary)), dtype=int)

    for words in documents:
        word_pairs = combinations([vocab_index[word] for word in words if word in vocab_index], 2)
        for i, j in word_pairs:
            cooccurrence_matrix[i][j] += 1
            cooccurrence_matrix[j][i] += 1

    return cooccurrence_matrix

# Function to create graph from co-occurrence matrix
def build_graph_from_matrix(cooccurrence_matrix, vocabulary):
    G = nx.Graph()

    # Add nodes
    for word in vocabulary:
        G.add_node(word)

    # Add edges with weights
    for i in range(len(vocabulary)):
        for j in range(i + 1, len(vocabulary)):
            if cooccurrence_matrix[i][j] > 0:
                G.add_edge(vocabulary[i], vocabulary[j], weight=cooccurrence_matrix[i][j])

    return G

# Directory containing the text documents
doc_dir = 'data'

# Load and preprocess documents
documents = load_and_preprocess_documents(doc_dir)

# Flatten list of words to build vocabulary
all_words = [word for doc in documents for word in doc]
vocabulary = sorted(list(set(all_words)))  # Unique words sorted alphabetically

# Define the file path
file_path = "vocabulary.txt"

# Save the vocabulary to a text file
with open(file_path, "w", encoding='utf-8') as f:
    for word in vocabulary:
        f.write(word + "\n")

# Assign an index to each word starting from 1
word_to_index = {word: idx + 1 for idx, word in enumerate(vocabulary)}

# Build co-occurrence matrix
cooccurrence_matrix = build_cooccurrence_matrix(documents, vocabulary)

# Build graph from co-occurrence matrix
G = build_graph_from_matrix(cooccurrence_matrix, vocabulary)

# Convert graph to specified format and save to .graph file
output_file = 'input.graph'

with open(output_file, 'w', encoding='utf-8') as file:
    # Write the first line with number of nodes, edges, and "1" for weighted
    file.write(f"{len(vocabulary)} {G.number_of_edges()} 1\n")

    # Write adjacency list with weights
    for node in range(1, len(vocabulary) + 1):
        neighbors = []
        for neighbor in G.neighbors(vocabulary[node - 1]):
            neighbor_index = word_to_index[neighbor]
            weight = G[vocabulary[node - 1]][neighbor]['weight']
            neighbors.extend([neighbor_index, weight])
        # Write the adjacency list for the current node
        file.write(" ".join(map(str, neighbors)) + "\n")

print(f"Graph saved to {output_file} in the specified format.")
