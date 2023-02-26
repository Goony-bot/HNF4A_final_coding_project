import requests
import sys
import json

server = "https://rest.ensembl.org"

# Prompt the user to enter the variant ID
variant_id = input("Enter the variant ID (e.g. ENST00000003084:c.1431_1433delTTC): ")

# Build the API request URL
ext = f"/vep/human/hgvs/{variant_id}"
url = server + ext
git
# Call the Ensembl VEP API to retrieve the variant effect data
headers = {"Content-Type": "application/json"}
response = requests.get(url, headers=headers)

# Check if the response was successful
if not response.ok:
    response.raise_for_status()
    sys.exit()

# Parse the JSON response and save it in a dictionary
decoded = response.json()
decoded_dict = json.loads(json.dumps(decoded, indent=4))

# Search for the "PolyPhen" score in the response
polyphen_score = None
for transcript in decoded_dict:
    for consequence in transcript["transcript_consequences"]:
        if "polyphen_score" in consequence:
            polyphen_score = consequence["polyphen_score"]
            break
    if polyphen_score is not None:
        break

# Print the PolyPhen score (if found)
if polyphen_score is not None:
    print(f"The PolyPhen score is: {polyphen_score}")
else:
    print("The PolyPhen score was not found in the response.")