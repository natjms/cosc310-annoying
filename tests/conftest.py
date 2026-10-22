import pytest
from dotenv import find_dotenv, load_dotenv

def pytest_configure(config):
    load_dotenv('.env.test')
    return config
