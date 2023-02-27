# in this iteration i have added an exception handeling block for the API
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
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() # raise an exception if the response is not OK
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    print (f"Please click on the link about to view the error that occurred")
    sys.exit()
except requests.exceptions.Timeout: #rasie an exception if the request times out before receiving a response from the server
    print("Error: Request timed out")
    sys.exit()
except requests.exceptions.ConnectionError: #raise an exception if the request cannot be sent due to a network connectivity issue, such as a DNS resolution failure or a refused connection
    print("Error: Could not connect to the server")
    sys.exit()
except requests.exceptions.HTTPError as e: #rasie an exception if the server responds with an HTTP error status code, such as 404 Not Found or 500 Internal Server Error.
    print(f"HTTP error {e.response.status_code}: {e.response.reason}")
    sys.exit()
except requests.exceptions.TooManyRedirects: #rasie an exception if the request exceeds the maximum number of allowed redirects
    print("Error: Too many redirects")
    sys.exit()
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    sys.exit()

# Parse the JSON response and save it in a dictionary
decoded = response.json()
decoded_dict = json.loads(json.dumps(decoded, indent=4))

print(json.dumps((decoded), indent=4))
