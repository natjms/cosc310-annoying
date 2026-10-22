import pytest
from dotenv import find_dotenv, load_dotenv

#@pytest.fixture(scope='module', autouse=True)
def pytest_configure(config):
    load_dotenv('.env.test')
    return config
