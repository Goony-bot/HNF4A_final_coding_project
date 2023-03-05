# automated testing using the pytest, this was done for sprint2_gm but there is an issue
# in matching the input to the output

import pytest
import requests
from unittest.mock import patch
from requests.exceptions import RequestException

class Conseq:
    def __init__(self, variant_id):
        self.variant_id = variant_id

    def get_consequence(self):
        try:
            url = f'https://rest.ensembl.org/vep/human/hgvs/{self.variant_id}?canonical=1;numbers=1;content-type=application/json'
            response = requests.get(url)
            data = response.json()
            if data is not None and ['primary_snapshot_data'] in data and ['placements_with_allele'][0]['alleles'][0]['allele'].startswith('T'):
                return "The specified variant leads to stop_gained and meets PVS1 criteria at a very strong level."
            else:
                return "PVS1 not met"
        except requests.exceptions.RequestException as e:
            raise e
            return None



class TestConseq:
    @pytest.mark.parametrize("variant_id, expected_output", [
        ("NC_000020.11:g.44406195C>T",
         "PVS1 not met"),
        ("NC_000020.11:g.44424208C>T", "PVS1 not met"),
    ])
    def test_get_consequence(self, variant_id, expected_output):
        conseq = Conseq(variant_id)
        assert conseq.get_consequence() == expected_output




def test_get_consequence_request_exception():
    with patch('requests.get', side_effect=RequestException):
        c = Conseq('variant_id')
        with pytest.raises(RequestException):
            c.get_consequence()


def test_get_consequence_no_data():
    with patch('requests.get', return_value=type('test', (object,), {'json': lambda: None})):
        c = Conseq('variant_id')
        assert c.get_consequence() == "PVS1 not met"


# Run the test for multiple variant IDs
def test_multiple_variants():
    variant_id = ["NC_000020.11:g.44406195C>T", "NC_000020.11:g.44424208C>T"]
    expected_output = ""
    for variant_id in variant_id:
        conseq = Conseq(variant_id)

