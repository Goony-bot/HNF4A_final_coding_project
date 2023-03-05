import requests
import sys
import logging
import json



logging.basicConfig(filename="logging.log", level=logging.DEBUG, format="%(asctime)s: %(levelname)s: %(message)s")


class Conseq:
    def get_most_severe_consequence(self, variant_id):
        server = "https://rest.ensembl.org"
        endpoint = f"/vep/human/hgvs/{variant_id}?canonical=1;numbers=1;content-type=application/json"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.get(server + endpoint, headers=headers)

            response.raise_for_status()  # raise an exception if the response is not OK
        except requests.exceptions.Timeout:
            logging.error('Request timed out')
            raise requests.exceptions.Timeout('Request timed out')
        except requests.exceptions.ConnectionError:
            logging.error('Could not connect to the server')
            raise requests.exceptions.ConnectionError('Could not connect to the server')
        except requests.exceptions.TooManyRedirects:
            logging.error('Too many redirects')
            raise requests.exceptions.TooManyRedirects('Too many redirects')
        except requests.exceptions.RequestException as e:
            logging.error(f'Request error: {e}')
            raise requests.exceptions.RequestException(f'Request error: {e}')

        data = response.json()
        decoded_data = json.loads(json.dumps(data, indent=4 ))

        print(decoded_data)

        if not data or not data[0]:  # empty list or dictionary returned by API
            logging.warning('No data returned by API')
            return None

        most_severe_consequence = data[0].get("most_severe_consequence")
        print(most_severe_consequence)

        if not most_severe_consequence:  # most_severe_consequence not found in API response
            logging.warning('No most_severe_consequence found in API response')
            return None
        for item in data[0]['transcript_consequences']:
            if 'cds_end' in item and 'exon' in item:

                #cds = data[0]['transcript_consequences'][0]['cds_end']

                cds_int = int(item['cds_end'])


                #exon = data[0]['transcript_consequences'][0]['exon']
                exon_split = int(item['exon'].split('/')[0])
                print(exon_split)
                break


        return most_severe_consequence








is_complete = False


while not is_complete:
    variant_id = input("Enter the variant ID in HGVS format: ")
    conseq = Conseq()

    try:
        most_severe_consequence= conseq.get_most_severe_consequence(variant_id)
        if most_severe_consequence:
            logging.info(f'Most severe consequence: {most_severe_consequence}')
            print(f"This variant leads to: {most_severe_consequence}")
            is_complete = True
        else:
            print("No most severe consequence found for the given variant ID")
    except Exception as e:
            logging.error(f"Error occurred: {e}")
            print(f"Error occurred: {e}")

server_2 = "https://rest.variantvalidator.org/"
ext_2 = f"https://rest.variantvalidator.org/VariantValidator/variantvalidator/GRCh38/{variant_id}/mane_select"
headers = {"Content-Type": "application/json"}

try:
    response_2 = requests.get(ext_2, headers=headers)
    decoded_2 = json.loads(response_2.content.decode())
    #print(decoded_2)
except requests.exceptions.RequestException as e:
    logging.error(f'Request error: {e}')
    raise requests.exceptions.RequestException(f'Request error: {e}')

def show_indices(obj, indices):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ('gene_symbol', 'mane_select', 'tlr', 'end_exon', 'start_exon'):
                yield indices + [k], v
            elif isinstance(v, (dict, list)):
                yield from show_indices(v, indices + [k])
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            if isinstance(v, (dict, list)):
                yield from show_indices(v, indices + [i])

for keys, v in show_indices(decoded_2, []):
    #print(keys, v)
    if 'gene_symbol' in keys:
        print("This gene is " + v)
    if 'mane_select' in keys:
        print('Is this transcript the mane select transcript? ' + str(v))
    if 'tlr' in keys:
        print('The protein change is ' + v)
   # if 'end_exon' in keys:    print('end exon: ' + str(v))<< keeping this on hold
    if 'start_exon' in keys:
        exon_number = v
        print(exon_number)












