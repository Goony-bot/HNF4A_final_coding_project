
# first we will import the modules that are required for the VEP API
import requests
import json
import sys



#the base URL to acess the ensembl REST_API, The REST API allows users to
# programmatically retrieve data from the Ensembl database using HTTP requests
server = "https://rest.ensembl.org"

# Prompt the user to enter the variant ID
variant_id = input("Enter the variant ID (e.g. ENST00000316673:c.281_282delinsC): ")

# Build the API request URL
ext = f"/vep/human/hgvs/{variant_id}"
url = server + ext

# Call the Ensembl VEP API to retrieve the variant effect data and the return in json

headers = {"Content-Type": "application/json"}
response = requests.get(url, headers=headers)

# Check if the response was successful
if not response.ok:
    response.raise_for_status()
    sys.exit()

# Parse the JSON response and save it in a dictionary
decoded = response.json()
decoded_dict = json.loads(json.dumps(decoded, indent=4))

print(json.dumps((decoded), indent=4))
