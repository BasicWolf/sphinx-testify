import os

extensions = [
    'sphinx_testify'
]

testify_from = [
    os.path.dirname(__file__) + '/test_results_1.xml',
    os.path.dirname(__file__) + '/test_results_2.xml'
]
