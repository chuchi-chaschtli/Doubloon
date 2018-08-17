import unittest

loader = unittest.TestLoader()
suite = loader.discover('.', pattern='*_tests.py')

runner = unittest.TextTestRunner()
runner.run(suite)