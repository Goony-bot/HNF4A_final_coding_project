# in this iteration i want to check if we are able to validate the varaint that the user has entered
# first we will import the modules that are required for the VEP API
import time

import requests
import sys
import json

# the base URL to acess the ensembl REST_API, The REST API allows users to
# programmatically retrieve data from the Ensembl database using HTTP requests
server = "https://rest.ensembl.org"

# Prompt the user to enter the transcript ID
transcript_id = input("Enter the transcript ID (e.g. ENST00000316673:c.281_282delinsC): ")

# Build the API request URL to check if the transcript ID is valid
lookup_url = f"{server}/lookup/id/{transcript_id}?expand=0"

# Call the Ensembl API to check if the transcript ID is valid
response = requests.get(lookup_url, headers={})

# Check if the response was successful
try:
    response.raise_for_status()  # raise an exception if the response is not OK
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    print("click on the link above to view the error")

# Parse the JSON response and check if the transcript ID was found
decoded = response.json()
if not decoded:
    raise ValueError("Transcript ID not found")

# Prompt the user to enter the variant ID
variant_id = input("Enter the variant ID (e.g. ENST00000316673:c.281_282delinsC): ")

# Build the API request URL
ext = f"/vep/human/hgvs/{transcript_id}:{variant_id}"
url = server + ext

# Call the Ensembl VEP API to retrieve the variant effect data and the return in json
response = requests.get(url, headers={"Content-Type": "application/json"})

# Check if the response was successful
if not response.ok:
    response.raise_for_status()
    sys.exit()

# Parse the JSON response and save it in a dictionary
decoded = response.json()
decoded_dict = json.loads(json.dumps(decoded, indent=4))

print(json.dumps((decoded), indent=4))
