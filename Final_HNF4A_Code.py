# This is the final code, essentially  this code

# Import all the modules that will be used for this code
import requests
import logging
import json

# Here we have the basic configuration for the logging module, anything that is DEBUG or higher will be logged
logging.basicConfig(filename="logging.log", level=logging.DEBUG, format="%(asctime)s: %(levelname)s: %(message)s")


class Conseq:  # this is our main function
    def get_most_severe_consequence(self, variant_id):  # here were pulling from the VEP URL based on a user input of
        # variant
        server = "https://rest.ensembl.org"  # This is the ensemble API point of access
        endpoint = f"/vep/human/hgvs/{variant_id}?canonical=1;numbers=1;content-type=application/json"
        headers = {"Content-Type": "application/json"}

        try:  # we have wrapped the response in a try except block so that we can handle exceptions and log them
            response = requests.get(server + endpoint, headers=headers)

            response.raise_for_status()  # raise an exception if the response is not OK
        except requests.exceptions.Timeout:
            logging.error('Request timed out')
            raise requests.exceptions.Timeout('Request timed out')
        except requests.exceptions.ConnectionError:  # raise an exception for connection error
            logging.error('Could not connect to the server')
            raise requests.exceptions.ConnectionError('Could not connect to the server')
        except requests.exceptions.TooManyRedirects:  # raise an exception for too many directs
            logging.error('Too many redirects')
            raise requests.exceptions.TooManyRedirects('Too many redirects')  # # raise an exception too many directs
        except requests.exceptions.RequestException as e:  # general error exception that will catch all
            logging.error(f'Request error: {e}')
            raise requests.exceptions.RequestException(f'Request error: {e}')

        # here we are collecting the HTTP json file response and parsing it to python
        data = response.json()
        decoded_data = json.loads(json.dumps(data, indent=4))

        # print(decoded_data) <this code is important during testing

        if not data or not data[0]:  # empty list or dictionary returned by API then log warning
            logging.warning('No data returned by API')
            return None
        # from the [data] json response we are getting the most severe consequence
        most_severe_consequence = data[0].get("most_severe_consequence")
        # print(most_severe_consequence) < this is used for testing only

        if not most_severe_consequence:  # most_severe_consequence not found in API response
            logging.warning('No most_severe_consequence found in API response')
            return None
        # here we are using a forloop that allows us to look into the returned json file and extract cds_end and exon #
        # we use a break to get the first exon number and cds_end in the list
        for item in data[0]['transcript_consequences']:
            if 'cds_end' in item and 'exon' in item:
                cds_int = int(item['cds_end'])
                print(f'The CDS_END for this variant is: ', {cds_int})
                exon_split = int(item['exon'].split('/')[0])
                print(f"This variant occurs in", {exon_split})
                break
        # defining the PVS1 criteria, we use an IF OR statement to set the PVS1 criteria for the HNF4A gene
        if most_severe_consequence == 'stop_gained' or most_severe_consequence == 'frameshift_variant':
            if exon_split < 10 and cds_int < 1258:
                print("This variant meets the PVS1 criteria at a very strong level")
            elif exon_split == 10 and cds_int in range(1258, 3180):
                print("This variant meets the PVS1 criteria at a supporting level")
            else:
                print("This variant does not meet PVS criteria")
        else:
            print("This variant does not meet PVS criteria")

        return most_severe_consequence


is_complete = False

# This while loop is used to check if there is an error in VEP API call then the user will be prompted to input the
# variant again
while not is_complete:
    variant_id = input("Enter the variant ID in HGVS format: ")
    conseq = Conseq()

    # This is another try an except error handling block, if the conseq didn't work
    try:
        most_severe_consequence = conseq.get_most_severe_consequence(variant_id)
        if most_severe_consequence:
            logging.info(f'Most severe consequence: {most_severe_consequence}')
            print(f"This variant leads to: {most_severe_consequence}")
            is_complete = True
        else:
            print("No most severe consequence found for the given variant ID")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")

# Here we call the VV API to get the protein, mane select transcript and gene name

server_2 = "https://rest.variantvalidator.org/"
ext_2 = f"https://rest.variantvalidator.org/VariantValidator/variantvalidator/GRCh38/{variant_id}/mane_select"
headers = {"Content-Type": "application/json"}

# This is an exception handling block for the VV API
try:
    response_2 = requests.get(ext_2, headers=headers)
    decoded_2 = json.loads(response_2.content.decode())
    # print(decoded_2)
except requests.exceptions.RequestException as e:
    logging.error(f'Request error: {e}')
    raise requests.exceptions.RequestException(f'Request error: {e}')


# Here we are indexing the VV json return and getting the information
# I found VV easier to get information than ensemble
def show_indices(obj, indices):  # function that will show the indices because I wasn't sure about them
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ('gene_symbol', 'mane_select', 'tlr', 'end_exon', 'start_exon'):
                yield indices + [k], v
            elif isinstance(v, (dict, list)):
                yield from show_indices(v, indices + [k])
                break
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, (dict, list)):
                yield from show_indices(v, indices + [i])
                break

# Printing the VV extracted information
for keys, v in show_indices(decoded_2, []):
    # print(keys, v)
    if 'gene_symbol' in keys:
        print("This gene is " + v)
    if 'mane_select' in keys:
        print('Is this transcript the mane select transcript? ' + str(v))
    if 'tlr' in keys:
        print('The protein change is ' + v)
    # if 'end_exon' in keys:    print('end exon: ' + str(v))<< keeping this on hold
    if 'start_exon' in keys:
        exon_number = v

