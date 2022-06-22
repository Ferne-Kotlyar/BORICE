from borice.application import *

# Test borice
def test_borice():
    app = Application()
    app.run("example_datafile.csv", num_steps=100, burn_in=1, seed=123)