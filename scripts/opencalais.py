"""

Author: Amy DiPierro
Version: 2020-02-15

A script using BeautifulSoup to parse and extract the first paragraph
in the "Reason for Recall section of each FDA product recall page downloaded
by fda.py, and then send the paragraph to the OpenCalais API for entity extraction.

USAGE:

From the command-line:

    python opencalais.py 

OUTPUT:

    JSON files of socialTags found by OpenCalais

"""

### Libraries to include

import requests
import bs4
import os
import json
import lxml

### Main

def get_opencalais():
    """
    Run this entire script.
    """
    api_key = os.environ["PERMID_API_KEY"]
    recall_graphs, full_paths = extract_recall_graph()
    json_list = send_to_opencalais(recall_graphs, api_key)
    download_json(json_list, full_paths)

### Get reason for recall paragraph

def extract_recall_graph():
    """
    Use BeautifulSoup to extract first "Reason for Recall" paragraph in each html
    """
    
    # Construct the raw_directory path
    project_root = os.environ['PYTHONPATH']
    raw_directory = '{}/data/raw/'.format(project_root)

    # Initialize list for "Reason for Recall" graphs
    recall_graphs = []
    
    # Initialize list for file paths
    full_paths = []
    
    for html in os.listdir(raw_directory):
        if html.endswith('.html'):
            
            # Construct the full file path
            full_path = '{}{}'.format(raw_directory, html)
            full_paths.append(full_path)
            
            # Open each HTML file
            with open(full_path, 'r') as local_file:
                
                # Turn into soup and get all graphs
                soup = bs4.BeautifulSoup(local_file, features="lxml")
                all_graphs = soup.body.main.article.find_all('p')

                # Filter to only the graphs we want
                for graph in all_graphs:
                    if 'is recalling' in graph.text:
                        recall_graphs.append(graph.text)
    
    return recall_graphs, full_paths

### Send to OpenCalais

def send_to_opencalais(recall_graphs, api_key):
    """
    Send the paragraph to OpenCalais for entity extraction.
    """
    json_list = []

    url = "https://api-eit.refinitiv.com/permid/calais"
    headers = {
        'Content-Type': "text/html",
        'X-AG-Access-Token': api_key,
        'outputformat': "application/json"
        }
    
    for recall_graph in recall_graphs:
        response = requests.request("POST", url, data=recall_graph, headers=headers)
        response_json = response.json()
        json_list.append(response_json)
    
    return json_list

### Download JSON files

def download_json(json_list, full_paths):
    """
    Save the JSON returned by OpenCalais in local files.
    """
    for item, path in zip(json_list, full_paths):
        path = path.strip('.html')
        json_path = '{}.json'.format(path)
        
        with open(json_path, 'w') as local_file:
            json.dump(item, local_file) 

if __name__ == "__main__":
    get_opencalais()