
# to run thsi test, in terminal input pytest test_pytest_final_code.py
import pytest
from Final_HNF4A_Code import Conseq

def test_get_most_severe_consequence(monkeypatch):
    # Set the value to be returned by the input() function
    monkeypatch.setattr('builtins.input', lambda _: 'NC_000020.11:g.44406195C>T')

    conseq = Conseq()
    most_severe_consequence = conseq.get_most_severe_consequence()
    assert most_severe_consequence == 'missense_variant'
