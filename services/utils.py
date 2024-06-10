import json
import os
import hashlib

# Function to read JSON data from a file
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to generate a hash from a URL
def hash_url(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()

# Function to check if a file already exists
def file_exists(directory, filename):
    files = os.listdir(directory)
    for file in files:
        if file.startswith(filename):
            return True
    return False

# Function to save content to a file
def save_content(directory, filename, content):
    # Create directory path
    os.makedirs(directory, exist_ok=True)
    
    # Create a filename from the hash of the URL
    file_path = os.path.join(directory, filename)
    
    # Write the dictionary to the file as JSON
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)
    
    return file_path