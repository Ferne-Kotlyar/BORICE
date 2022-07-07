import yaml
import hashlib
import pytest

from borice.application import *

def hashfile(filename):
	BLOCKSIZE = 65536
	hasher = hashlib.sha1()
	with open(filename, 'r') as f:
		while True:
			data = f.read(BLOCKSIZE)
			if not data:
				break
			hasher.update(data.encode())
	return hasher.hexdigest()

def getOrDefault(dict, key, default):
	if key in dict:
		return dict[key]
	else:
		return default

def evaluateTest(app, test):
	# Pass the args to BORICE except the hash (result)
	args = {key:test[key] for key in test if key != 'hash'}
	app.run(**args)
	hash = hashfile('BORICE_output1.txt')

	# If the test has no saved hash, register it
	if not 'hash' in test:
		test['hash'] = hash
		return 1

	assert hash == test['hash']
	return 0

# Test borice
def test_output_validation():
	app = Application()
	validationFile = 'validation.yml'
	newTests = 0

	# Try running test cases
	with open(validationFile, 'r') as file:
		tests = yaml.safe_load(file)
		for test in tests:
			newTests += evaluateTest(app, test)

	# Add the computed hash to tests with no hash result
	if newTests > 0:
		with open(validationFile, 'w') as file:
			yaml.safe_dump(tests, file, default_flow_style=False, sort_keys=False)