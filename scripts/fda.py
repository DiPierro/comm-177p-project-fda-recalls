"""

Author: Amy DiPierro
Version: 2020-02-14

A script to scrape the links to 2020 medical device recall announcements,
then request and save the raw HTML of each detail page.

USAGE:

From the command-line:

    python fda.py

OUTPUT:

    Raw HTML of each detail page.

"""

### Libraries to include

import requests
import bs4
import os

### Main

def download_html():
    """
    Run this entire script.
    """
    html = get_root()
    end_links = get_links(html)
    download_detail_page(end_links)

### Access root page

def get_root():
    """
    Get the root URL link.
    """
    url = "https://www.fda.gov/medical-devices/medical-device-recalls/2020-medical-device-recalls"
    response = requests.get(url)
    html = response.text
    return html
    
### Get links to detail pages

def get_links(html):
    """
    Make a list of links to scrape
    """
    soup = bs4.BeautifulSoup(html, 'lxml')
    links = soup.table.find_all('a')
    end_links = []

    for link in links:
      if '/medical-devices/medical-device-recalls/' in link.attrs['href']:
        end_link = link.attrs['href']
        end_links.append(end_link)

    return end_links
    
### Download each detail page

def download_detail_page(end_links):
    """
    Save the raw HTML for each detail page to the data/raw/ directory.
    """

    root_link = 'https://www.fda.gov'
    recall_links = []
    project_root = os.environ['PYTHONPATH']
        
    for end_link in end_links:
      
      # Construct short link to name the file.
      short_link = end_link[40:]
      
      # Construct link to download the html, then download it.
      full_link = "{}{}".format(root_link, end_link) 
      detail_response = requests.get(full_link)
      detail_html = detail_response.text
      html_file = '{}/data/raw/{}.html'.format(project_root, short_link)
      with open(html_file, 'w') as local_file:
        local_file.write(detail_html)
    
if __name__ == "__main__":
    download_html()