
from app.request_helper import send_bitbucket_request, send_github_request

from unittest.mock import patch
import app

bitbucket_root_url = 'https://api.bitbucket.org/2.0/'
github_root_url = 'https://api.github.com/'


class TestGitProfile:
    """
    unit tests for the git profile helper methods
    """

    @patch('app.request_helper.send_github_request')
    def test_send_get_request_to_github(self,send_get_request):
        from app.request_helper import send_github_request
        app.request_helper.send_github_request(github_url=github_root_url)

        assert app.request_helper.send_github_request == send_get_request
        app.request_helper.send_github_request.assert_called_once_with(github_url=github_root_url)

    @patch('app.request_helper.send_bitbucket_request')
    def test_send_get_request_to_bitbucket(self,send_get_request):
        from app.request_helper import send_github_request
        app.request_helper.send_bitbucket_request(bitbucket_url=bitbucket_root_url)
        assert app.request_helper.send_bitbucket_request == send_get_request
        app.request_helper.send_bitbucket_request.assert_called_once_with(bitbucket_url=bitbucket_root_url)
