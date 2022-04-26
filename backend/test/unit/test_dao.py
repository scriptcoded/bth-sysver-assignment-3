from more_itertools import side_effect
from src.util.validators import getValidator
from src.util.dao import DAO
from src.controllers.usercontroller import UserController

from unittest import mock
import pytest

@pytest.fixture
def sut(request):
    collection_name = request.param[0]
    validator_name = request.param[1]

    # Mocked getValidator so that we can control what validator to use
    # regardless of the collection name
    def mocked_getValidator(_: str):
        return getValidator(validator_name)

    # Patch getValidator in src.util.dao to use our mocked getValidator
    with mock.patch('src.util.dao.getValidator', side_effect=mocked_getValidator):
        sut = DAO(collection_name)

        yield sut

        sut.drop()

# Parameter order: collection_name, validator_name
@pytest.mark.parametrize('sut', [('test', 'user')], indirect=True)
def test_create(sut):
    model = {
        'firstName': 'test',
        'lastName': 'hallo',
        'email': 'oke',
        'tasks': []
    }

    result = sut.create(model)
    print('Hello!')
    print(result)
    # assert result == model
