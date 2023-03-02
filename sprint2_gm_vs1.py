# building on Ghadir's work in iteration_6g to add further functions.

import requests
import logging
import json
# needed to make the user input URL-friendly
from urllib.parse import quote


logging.basicConfig(filename="logging.log", level=logging.DEBUG, format="%(asctime)s: %(levelname)s: %(message)s")


class Conseq:
    # added __init__ method to initialise attributes
    def __init__(self, variant_id):
        self.variant_id = quote(variant_id)
        self.url = f"https://rest.ensembl.org/vep/human/hgvs/{self.variant_id}?canonical=1;numbers=1;content-type=application/json"

#changed function name as we are no longer looking for the 'most severe conseq' since we'll be looking at the canonical transcript only
    def get_consequence(self):
        try:
            response = requests.get(self.url)

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
            print(f'Request error: {e}')
            raise requests.exceptions.RequestException(f'Request error: {e}')

        data = response.json()
        decoded_data = json.loads(json.dumps(data, indent=4))
        decoded_1 = decoded_data[0].get('transcript_consequences')
        #print(decoded_1)
        if not data:  # empty list or dictionary returned by API
            logging.warning('No data returned by API')
            return None

# create a dictionary showing properties of transcript that meets criteria HNF4A, canonical, exon 1-9, <c.1258
        can_hnf4a_dict1 = [d for d in decoded_1
                            if d.get('gene_symbol') == 'HNF4A'
                            and d.get('canonical') == 1
                            and (int(d.get('exon', 0).split('/')[0]) < 10 or int(d.get('cds_end', 0)) < 1258)],

        can_hnf4a_dict2 = [d2 for d2 in decoded_1
                            if d2.get('gene_symbol') == 'HNF4A'
                            and d2.get('canonical') == 1
                            and int(d2.get('cds_end', 0)) == range(1257, 3180)]

# message to be printed for variants not
        #if not can_hnf4a_dict1 or can_hnf4a_dict2:
                #print('PVS1 not met')

        for d in can_hnf4a_dict1:
                rel_dict = can_hnf4a_dict1[0][0]
                #print(rel_dict)
                variant_type_ = rel_dict.get('consequence_terms')
                variant_type = variant_type_[0]
                if variant_type == 'stop_gained' or 'frameshift_variant':
                    print(f"The specified variant leads to {variant_type} and meets PVS1 criteria at a very strong level.")

        for d in can_hnf4a_dict2:
                rel_dict2 = can_hnf4a_dict2[0]
                #print(rel_dict)
                variant_type2_ = rel_dict2.get('consequence_terms')
                variant_type2 = variant_type2_[0]
                if variant_type2 == 'stop_gained' or 'frameshift_variant':
                    print(f"The specified variant leads to {variant_type2} and meets PVS1 criteria at a supporting level.")

def __repr__(self):
        return f"Conseq({self.variant_id})"


is_complete = False

while not is_complete:
    variant_id = input("Enter the variant ID in HGVS format: ")
    conseq = Conseq(variant_id)
    conseq.get_consequence()
