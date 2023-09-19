import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import pytest
import sys, os

# SET UP SRC LIBRARY FOR TESTINGS
current_library = os.getcwd()
sys.path.append(current_library+"/src")
logger.info(f"Current Library: {current_library}")
logger.info(f"Project Paths: {sys.path}")


from unittest.mock import patch
from components.db_api import DbApi

@pytest.fixture(scope="session")
def db_fixture()-> DbApi:
    db_instance = DbApi(user="root", password="1234", host="127.0.0.1", database="timer_db")

    yield db_instance

    db_instance = ""    