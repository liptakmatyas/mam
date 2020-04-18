import os

import pytest


DIR_OF_THIS_FILE=os.path.dirname(os.path.abspath(__file__))

TESTS_ROOT='{}/tests'.format(DIR_OF_THIS_FILE)
TEST_INPUT_FILE_ROOT='{}/test_files'.format(TESTS_ROOT)

@pytest.fixture
def test_input():
    def _test_input_path(rel_path):
        return "{}/{}".format(TEST_INPUT_FILE_ROOT, rel_path)

    return _test_input_path

