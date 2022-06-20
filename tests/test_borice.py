from borice.application import *

# Test borice with default parameters
def test_borice():
    Application().run("example_datafile.csv", [True, True, True])