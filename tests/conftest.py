import pytest
from .mock_data import merged_data
import app

@pytest.fixture()
def app(request):
    app_ = app
    return app_

@pytest.fixture()
def send_get_request(request):
    expected_output = ("<Response [200]>", None)
    return expected_output


@pytest.fixture()
def send_bitbucket_request(request):
    expected_output = ("<Response [200]>", None)
    return expected_output

@pytest.fixture()
def successful_request(request):
    expected_ouput = merged_data
    return expected_ouput
