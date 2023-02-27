# in this code I have modified the exception handeling block to include netwrok error and if the varaint is not found
# in the the ensemble API first we will import the modules that are required for the VEP API
import requests
import json
import sys
import logging

logging.basicConfig(filename="logging.log", level=logging.DEBUG, format="%(asctime)s: %(levelname)s: %(message)s")

# the base URL to acess the ensembl REST_API, The REST API allows users to
# programmatically retrieve data from the Ensembl database using HTTP requests
server = "https://rest.ensembl.org"

# Prompt the user to enter the variant ID
variant_id = input("Enter the variant ID (e.g. ENST00000316673:c.281_282delinsC): ")

# Build the API request URL
ext = f"/vep/human/hgvs/{variant_id}"
url = server + ext

# Call the Ensembl VEP API to retrieve the variant effect data and the return in json
headers = {"Content-Type": "application/json"}

# Check if the response was successful, error handleing and exceptions
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # raise an exception if the response is not OK
except requests.exceptions.Timeout:  # raise an exception if the request times out before receiving a response from
    # the server
    logging.error('Request timed out')  # here i am logging the exception errors
    print("Error: Request timed out")
except requests.exceptions.ConnectionError:  # raise an exception if the request cannot be sent due to a network
    # connectivity issue, such as a DNS resolution failure or a refused connection
    logging.error('Could not connect to the server')  # here i am logging the exception errors
    print("Error: Could not connect to the server")
except requests.exceptions.TooManyRedirects:  # raise an exception if the request exceeds the maximum number of
    # allowed redirects
    logging.error('Too many redirects')  # here i am logging the exception errors
    print("Error: Too many redirects")
except requests.exceptions.RequestException as e:  # raise all other exceptions (i have put the specifc exceptions
    # first)

    error_message = f": {e}\nRequest URL : {url}"
    print(
        "check that you have entered the correct variant, click the link to view detailed error message " + error_message)
    print("only HGVS is accepted eg.ENST00000316673:c.281_282delinsC  ")
    logging.error(error_message)

# Parse the JSON response and save it in a dictionary
decoded = response.json()
decoded_dict = json.loads(json.dumps(decoded, indent=4))

print(json.dumps((decoded), indent=4))
