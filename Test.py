import unittest
from unittest.mock import patch
from Iteration_6G import Conseq


class TestConseq(unittest.TestCase):

    @patch('Iteration_6G.requests.get')
    def test_get_most_severe_consequence(self, mock_get):
        variant_id = "NC_000023.11:g.284253C>G"
        mock_get.return_value.json.return_value = [{"most_severe_consequence": "missense_variant"}]
        conseq = Conseq()
        result = conseq.get_most_severe_consequence(variant_id)
        self.assertEqual(result, "missense_variant")

if __name__ == '__main__':
    unittest.main()
