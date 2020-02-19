"""

Author: Amy DiPierro
Version: 2020-02-18

A script that imports the top-level functions from each of the prior modules 
and runs them inside a main function.

USAGE:

From the command-line:

    python run_pipeline.py

OUTPUT:

    * fda_tags.csv
    * JSON files of socialTags found by OpenCalais
    * Raw HTML of each detail page

"""

### Libraries to include

from fda import download_html
from opencalais import get_opencalais
from report import download_report

### Main

def main():
    """
    Run the three scripts in this project.
    """
    download_html()
    get_opencalais()
    download_report()
    
if __name__ == '__main__':
    main()