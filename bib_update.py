#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 18:56:16 2023
@author: Olivechu
"""
# import bibcure
# revised from https://github.com/bibcure/title2bib
import bibtexparser
import requests
from fuzzywuzzy import fuzz, process
from Levenshtein import distance
import re

path = '/Users/Research/thesis/backup/'
bare_url = "http://api.crossref.org/"

# Load the .bib file
with open(path + 'mythesis.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    
def fetch_doi(title):
    crossref_url = "https://api.crossref.org/works"
    response = requests.get(crossref_url, params={"query": title, "rows": 1})
    if response.status_code == 200:
        data = response.json()
        if data["message"]["total-results"] > 0:
            return data["message"]["items"][0]["DOI"]
    return None

def fetch_bib_entry_from_doi(doi):
    url = f"https://doi.org/{doi}"
    headers = {"Accept": "application/x-bibtex"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

for entry in bib_database.entries:
    # Check for missing DOI and fetch it
    if "doi" not in entry:
        doi = fetch_doi(entry["title"])
        print('update:'  + doi)
        # print
        if doi:
            entry["doi"] = doi


    # Normalize other fields (e.g., author names, journal names) using fuzzy matching or other techniques

# Save the normalized .bib file
with open(path + 'normalized_bib_file.bib', 'w') as bibtex_file:
    bibtexparser.dump(bib_database, bibtex_file)
    
with open(path + 'normalized_bib_file.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)
    # new_bib = update_bibs_from_doi(bibtex_file)

for entry in bib_database.entries:
    # If the entry has a DOI, fetch the latest bib entry using the DOI
    if "doi" in entry:
        bib_entry_str = fetch_bib_entry_from_doi(entry["doi"])
        if bib_entry_str:
            # Parse the fetched bib entry and update the original entry
            fetched_entry = bibtexparser.loads(bib_entry_str).entries[0]
            entry.update(fetched_entry)

# Save the updated .bib file
with open('updated_bib_file.bib', 'w') as bibtex_file:
    bibtexparser.dump(bib_database, bibtex_file)
