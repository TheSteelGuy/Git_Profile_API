import pytest
from .mock_data import merged_data, languages


@pytest.fixture()
def send_get_request(request):
    expected_output = ("<Response [200]>", None)
    return expected_output


@pytest.fixture()
def successful_request(request):
    expected_ouput = merged_data
    return expected_ouput


@pytest.fixture()
def repo_type(request):
    expected_output = dict(total_original_repos=2, total_forked_repos=10)
    return expected_output


@pytest.fixture()
def repo_follower(request):
    expected_output = 4
    return expected_output


@pytest.fixture()
def languages_list(request):
    expected_output = languages
    return expected_output


@pytest.fixture()
def repo_topic(request):
    expected_output = ['Kotlin', 'Data Structures']
    return expected_output

