# Define file paths
vocab_file = 'vocabulary.txt'
cluster_file = 'input.graph.part.200'
output_file = 'top_20_words.txt'

# Initialize dictionaries to store clusters
clusters = {}

# Step 1: Read vocabulary and cluster files
with open(vocab_file, 'r') as vf, open(cluster_file, 'r') as cf:
    vocab_lines = vf.readlines()
    cluster_lines = cf.readlines()

# Check if both files have the same number of lines
if len(vocab_lines) != len(cluster_lines):
    raise ValueError("Vocabulary and Cluster files should have the same number of lines")

# Step 2: Group words by cluster index
for word, cluster in zip(vocab_lines, cluster_lines):
    cluster_id = int(cluster.strip())  # Convert cluster index to integer
    word = word.strip()  # Strip any extra spaces or newline characters
    
    # Initialize list for the cluster if it doesn't exist
    if cluster_id not in clusters:
        clusters[cluster_id] = []
    
    # Append word to corresponding cluster list
    clusters[cluster_id].append(word)

# Step 3: Write top 20 words per cluster to output file
with open(output_file, 'w') as of:
    for cluster_id in sorted(clusters.keys()):  # Sort clusters by cluster ID
        top_words = clusters[cluster_id][:20]  # Get top 20 words in the cluster
        of.write(f"cluster {cluster_id + 1}:\n")  # Format cluster header
        
        # Write each word in the cluster
        for word in top_words:
            of.write(f"   {word}\n")
        
        of.write("\n")  # New line between clusters

print(f"Top 20 words per cluster have been saved to {output_file}")
