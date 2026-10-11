import pytest
from dotenv import find_dotenv, load_dotenv

@pytest.fixture(autouse=True)
def load_test_dotenv():
	load_dotenv(find_dotenv('test.env'))
