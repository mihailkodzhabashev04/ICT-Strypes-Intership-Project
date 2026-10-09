
"""
The purpose of this file is to save the scraped data to a file.
The file name is  build in main.py(with a timestamp), so every
scrape creates a new file and nothing gets overwritten.
"""

import json
from pathlib import Path

def save_json(records, output_path):

    """
    Write a list of records to a JSON file
    and return its path.
    """

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:

        json.dump(records, file, ensure_ascii=False, indent=4)

    return path