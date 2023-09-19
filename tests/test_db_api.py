from datetime import datetime
import pytest
import uuid
from fastapi import HTTPException

from components.db_api import db_instance
from components.db_api import DbApi

def test_insert_timer(db_fixture: DbApi):
    try:
        timer_id = db_fixture.insert_timer("someurl",datetime.now())
    except Exception as err:
        pytest.fail(f"Failed to insert timer: {err}")
    try:
        uuid.UUID(timer_id)
        assert True
    except Exception as err:
        pytest.fail(f"The returned value is not uuid")
       
def test_get_timer_existing_timer(db_fixture: DbApi):
    # SETUP
    try:
        timer_id = db_fixture.insert_timer("test_get_timer", datetime.now())
    except Exception as err:
        pytest.fail("Couldn't finish the test's setup")

    # Assert
    response = db_fixture.get_timer_information(timer_id)

    # Assert
    assert response.timer_id==timer_id
    assert type(response.timer_status)==str
    assert type(response.timer_date)==datetime

def test_get_timer_non_existing_timer(db_fixture: DbApi):
    # SETUP
    try:
        timer_id = str(uuid.uuid4())
    except Exception as err:
        pytest.fail("Couldn't finish the test's setup")

    # Assert
    response = db_fixture.get_timer_information(timer_id)

    # Assert
    assert response==None

def test_get_timer_illegal_uuid(db_fixture: DbApi):
    # SETUP
    try:
        timer_id = "I'm not a uuid"
    except Exception as err:
        pytest.fail("Couldn't finish the test's setup")

    # Assert
    with pytest.raises(HTTPException) as excinfo:
        response = db_fixture.get_timer_information(timer_id)

    # Assert
    assert excinfo.value.detail == "Illegal UUID"