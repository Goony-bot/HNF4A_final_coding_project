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
my_dict = decoded[0]
# define also the key of interest...
key1 = 'most_severe_consequence'

# and the corresponding values of interest
frameshift = 'frameshift_variant'
nonsense = 'stop_gained'

# Boolean included for loop purpose
match_found = False

# we write a loop to determine if the variants of interest are specified as the most severe consequence.

for key, value in my_dict.items():
    #define the key
    if key == key1:
        # if the variant is frameshift or nonsense, a message is printed out indicating so.
        if value == frameshift or value == nonsense:
            match_found = True
            print('Variant type: ' + value)
            break
#if it's any other variant type, this message is printed.
        else:
            print('This is not a nonsense or frameshift variant.')

# for nonsense and frameshift variants, we need to find out where the premature termination occurs...

# this step uses VV rest-api
server_vv = "https://rest.variantvalidator.org/VariantValidator/variantvalidator/hg38/"
ext3 = "/refseq_select"
url_vv = server_vv + variant_id + ext3

try:
    response2 = requests.get(url_vv)
    response2.raise_for_status()  # raise an exception if the response is not OK
except requests.exceptions.Timeout:  # rasie an exception if the request times out before receiving a response from the server
    print("Error: Request timed out")

    sys.exit()

# Parse the JSON response and save it in a dictionary
decoded2 = response2.json()
decoded2_dict = json.loads(json.dumps(decoded, indent=4))


# print(json.dumps((decoded2), indent=4))

#to get the exon at which the variant occurs.
def get_start_exon(d, pattern):
    for key, value in d.items():
        if isinstance(value, dict):
            result = get_start_exon(value, pattern)
            if result is not None:
                return result
        elif key == pattern:
            return value


start_exon = get_start_exon(decoded2, 'start_exon')
print("The variant causes a premature termination at exon: " + start_exon)

#we are interested in variants occuring at exons 1-9...
#exon no. needs to be converted from str to int

start_exon_int = int(start_exon)

#function to check if exon 1-9 criteria satisfied.
def func_pvs1(start_exon_int):
    if start_exon_int < 10:
        print("This variant satisfies PVS1 at a very strong level.")

pvs1_outcome = func_pvs1(start_exon_int)

# next step is to filter variants occuring in exon 10.


