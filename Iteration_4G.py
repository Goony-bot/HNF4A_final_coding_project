# in this code I have modified the exception handeling block to include netwrok error and if the varaint is not found
# in the the ensemble API first we will import the modules that are required for the VEP API
import requests
import json
import sys

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

# Check if the response was successful
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # raise an exception if the response is not OK
except requests.exceptions.Timeout:  # rasie an exception if the request times out before receiving a response from the server
    print("Error: Request timed out")
    sys.exit()
except requests.exceptions.ConnectionError:  # raise an exception if the request cannot be sent due to a network connectivity issue, such as a DNS resolution failure or a refused connection
    print("Error: Could not connect to the server")
    sys.exit()
except requests.exceptions.TooManyRedirects:  # rasie an exception if the request exceeds the maximum number of allowed redirects
    print("Error: Too many redirects")
    sys.exit()
except requests.exceptions.RequestException as e: # raise all other exceptions , i have put the specifc exceptions first
    error_message = f": {e}\nRequest URL : {url}"
    print(
        "check that you have entered the correct varaint, click the link to view detailed error message " + error_message)
    print("only HGVS is accepted eg.ENST00000316673:c.281_282delinsC  ")

    sys.exit()

# Parse the JSON response and save it in a dictionary
decoded = response.json()
decoded_dict = json.loads(json.dumps(decoded, indent=4))

#print(json.dumps((decoded), indent=4))

# from the VEP output, we need to get the 'most_severe_consequence' value.
# to access the dictionary:
dict = decoded[0]
# define also the key of interest...
key1 = 'most_severe_consequence'

# and the corresponding values of interest
frameshift = 'frameshift_variant'
nonsense = 'stop_gained'

# Boolean included for loop purpose
match_found = False

# we write a loop to determine if the variants of interest are specified as the most severe consequence.

for key, value in dict.items():
    #define the key
    if key == key1:
        # if the variant is frameshift or nonsense, a message is printed out indicating so.
        if value == frameshift or value == nonsense:
            match_found = True
            print('Variant type: ' + value)
            break

# I have yet to determine the best way to print a statement when it's not nonsense or frameshift.

#if it's any other variant type, this message is printed.
    #else:
        #print('This is not a nonsense or frameshift variant.')


    #if not match_found:
       # print('This is not a nonsense or frameshift variant.')


