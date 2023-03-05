import requests
import sys
import logging
import json


logging.basicConfig(filename="logging.log", level=logging.DEBUG, format="%(asctime)s: %(levelname)s: %(message)s")


class Conseq:
    def get_most_severe_consequence(self, variant_id):
        server = "https://rest.ensembl.org"
        endpoint = f"/vep/human/hgvs/{variant_id}"
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
        if not data:  # empty list or dictionary returned by API
            logging.warning('No data returned by API')
            return None
        most_severe_consequence = data[0].get("most_severe_consequence")
        if not most_severe_consequence:  # most_severe_consequence not found in API response
            logging.warning('No most_severe_consequence found in API response')
            return None

        return most_severe_consequence



is_complete = False


while not is_complete:
    variant_id = input("Enter the variant ID in HGVS format: ")
    conseq = Conseq()

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

