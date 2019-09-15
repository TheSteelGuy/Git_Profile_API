from unittest.mock import patch
import app
from app.request_helper import handle_api_response

bitbucket_root_url = 'https://api.bitbucket.org/2.0/repositories/pytest'
github_root_url = 'https://api.github.com/pytest/repos'


class TestGitProfile:
    """
    unit tests for the git profile helper methods
    note that we we patch the functions so that we dont call any external service
    patching allow us to define the behaviour of our code and controll what happens
    """

    @patch('app.request_helper.send_github_request')
    def test_send_get_request_to_github_succeeds(self,send_get_request):
        """

        :param send_get_request: a fixture to prepare what the send_bitbucket_request function returns
        :return: send_get_request: a fixture to prepare what the send_github_request function returns
        """
        from app.request_helper import send_github_request
        app.request_helper.send_github_request(github_url=github_root_url)

        assert app.request_helper.send_github_request == send_get_request
        app.request_helper.send_github_request.assert_called_once_with(github_url=github_root_url)

    @patch('app.request_helper.send_bitbucket_request')
    def test_send_get_request_to_bitbucket_succeeds(self, send_get_request):
        """
        tests calls to the bitbucket api
        :param send_get_request: a fixture to prepare what the send_bitbucket_request function returns
        :return: None
        """
        from app.request_helper import send_github_request
        app.request_helper.send_bitbucket_request(bitbucket_url=bitbucket_root_url)
        assert app.request_helper.send_bitbucket_request == send_get_request
        app.request_helper.send_bitbucket_request.assert_called_once_with(bitbucket_url=bitbucket_root_url)

    @patch('app.request_helper.handle_api_response')
    def test_handle_api_response_returns_expected_values(self, successful_request):
        """
        tests handle api function
        :param successful_request: a fixture to prepare what the handle_api_response function returns
        :return: None
        """

        app.request_helper.handle_api_response(github_url=github_root_url, bitbucket_url=github_root_url)
        assert app.request_helper.handle_api_response == successful_request
        app.request_helper.handle_api_response.assert_called_once_with(github_url=github_root_url, bitbucket_url=github_root_url)

    @patch('app.request_helper.repo_types')
    def test_repo_types_returns_expected_values(self, repo_type, send_get_request):
        """
        tests repo types function
        :param repo_type: a fixture to prepare what the repo_types function returns
        :param send_get_request:
        :return: None
        """
        from app.request_helper import repo_types
        app.request_helper.repo_types(github_response=send_get_request, bitbucket_response=send_get_request)
        assert app.request_helper.repo_types == repo_type
        app.request_helper.repo_types.assert_called_once_with(github_response=send_get_request, bitbucket_response=send_get_request)

    @patch('app.request_helper.language_list')
    def test_language_list_returns_expected_values(self, languages_list, send_get_request):
        """
        tests language list function
        :param languages_list: fixture to prepare what the languages_list function returns
        :param send_get_request:
        :return: None
        """
        from app.request_helper import language_list
        app.request_helper.language_list(github_response=send_get_request, bitbucket_response=send_get_request)
        assert app.request_helper.language_list == languages_list
        app.request_helper.language_list.assert_called_once_with(github_response=send_get_request, bitbucket_response=send_get_request)

    @patch('app.request_helper.repo_topics')
    def test_repo_topics_returns_expected_values(self, repo_topic, send_get_request):
        """
        tests repo topics function
        :param repo_topic: fixture to prepare what the repo_topics function returns
        :param send_get_request:
        :return: None
        """
        from app.request_helper import repo_topics
        app.request_helper.repo_topics(github_response=send_get_request, bitbucket_response=send_get_request)
        assert app.request_helper.repo_topics == repo_topic
        app.request_helper.repo_topics.assert_called_once_with(github_response=send_get_request, bitbucket_response=send_get_request)




