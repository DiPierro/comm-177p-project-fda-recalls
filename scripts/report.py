"""

Author: Amy DiPierro
Version: 2020-02-15

A script that reads the JSON files downloaded by opencalais.py
and generates a CSV called fda_tags.csv.

USAGE:

From the command-line:

    python report.py 

OUTPUT:

    JSON files of socialTags found by OpenCalais

"""

### Libraries to include

import bs4
import os
import json
import csv

### Main

def download_report():
    """
    Run this entire script.
    """
    entities = get_names()
    save_csv(entities)

### Get names

def get_names():
    """
    Get the names of every socialTag.
    """

    #Initialize entities dictionary
    entities = {'entity': 'source_file'}

     # Construct the raw_directory path
    project_root = os.environ['PYTHONPATH']
    raw_directory = '{}/data/raw/'.format(project_root)
    
    for file in os.listdir(raw_directory):
        if file.endswith('.json'):
            
            # Construct the full file path
            full_path = '{}{}'.format(raw_directory, file)
            
            # Open each JSON file
            with open(full_path, 'r') as source_file:
                data = source_file.read()
                parsed_data = json.loads(data)
                
                # Iterate through the dictionary parsed_data
                for key in parsed_data:
                  if 'SocialTag' in key:
                      name = parsed_data[key]['name']
                      entities.update({name: file})

    return entities

### Save .csv

def save_csv(entities):
    """
    Create a csv at data/processed/fda_tags.csv.
    """
    project_root = os.environ['PYTHONPATH']

    with open('{}/data/processed/fda_tags.csv'.format(project_root), 'w', newline="") as output_file:
      writer = csv.writer(output_file)
      for entity, file_name in entities.items():
         writer.writerow([entity, file_name])

if __name__ == "__main__":
    download_report()