"""
The command to run the tests via command line
pytest test_01_examples.py -k "test_check_math"
"""


class TestExample:
    def test_check_math_1(self):
        a = 5
        b = 9
        assert a + b == 14, "Calculation is wrong"

    def test_check_math_2(self):
        a = 5
        b = 11
        assert a + b == 15, "Calculation is wrong"
