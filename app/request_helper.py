import requests
import aiohttp
import ssl
import asyncio


def send_github_request(github_url=''):
    """
    Sends requests to github
    :param github_url: github url
    :return: dict
    """
    github_req = None
    error = None
    try:
        # the documentations uses v3 by default but they advice that you explicitly specify the version as such
        github_req = requests.get(
            headers={'content-type': 'application/json', 'accept': 'Accept: application/vnd.github.v3+json'},
            url=github_url)
    except requests.exceptions.ConnectionError:
        error = 'Check your internet connection and try again, we could not send a request to Github'
    except:
        error = 'An error occurred with request to Github please try again'
    return github_req, error


def send_bitbucket_request(bitbucket_url=''):
    """
    Sends requests to bitbucket
    :param bitbucket_url: bitbucket url
    :return: dict
    """
    bitbucket_req = None
    error = None
    try:
        bitbucket_req = requests.get(
            headers={'content-type': 'application/json'},
            url=bitbucket_url)
    except requests.exceptions.ConnectionError:
        error = 'Check your internet connection and try again, we could not send a request to Bitbucket'
    except:
        error = 'An error occurred with request to Bitbucket please try again'

    return bitbucket_req, error


def handle_api_response(github_url='', bitbucket_url=''):
    """
    Function responsible for handling github and bitbucket api responses
    It also merges result from all the other functions
    :param github_url: github url
    :param bitbucket_url: bitbucket url
    :return: dict
    """

    # call the functions to get responses from github and bitbucket
    github_res, github_error = send_github_request(github_url)
    bitbucket_res, bitbucket_error = send_bitbucket_request(bitbucket_url)

    errors = [bitbucket_error, github_error]
    # Remove None from the list in-case everything went well with with the two api calls(bitbucket and Github)
    errors[:] = [error for error in errors if error is not None]

    merged_result = {
        'repo_types': repo_types(github_res, bitbucket_res),
        'total_watchers': repo_followers(github_res, bitbucket_res),
        'languages': language_list(github_res, bitbucket_res),
        'topics': repo_topics(github_res),
        'errors': errors
    }
    return merged_result


def repo_types(github_response, bitbucket_response):
    """
    :param github_response: response from github
    :param bitbucket_response: response from bitbucket
    :return: dict
    """
    count_original_repos = 0
    count_forked_repos = 0

    # check if the response was a success before any further processing
    if github_response is not None and github_response.status_code == 200:
        github_response_json = github_response.json()
        # filter repos with key fork as false, they are original repos
        original_repos = list(filter(lambda repo: repo['fork'] is False, github_response_json))
        count_original_repos += len(original_repos)
        count_forked_repos += len(github_response_json) - count_original_repos
    if bitbucket_response is not None and bitbucket_response.status_code == 200:
        bitbucket_response_json = bitbucket_response.json()
        # size gives the total repos
        total_repos = bitbucket_response_json['size']
        try:
            # filter to find repos which are forked
            forked_repos = list(filter(lambda repo: repo['parent'], bitbucket_response_json['values']))
            count_original_repos += total_repos - len(forked_repos)
        except KeyError:
            # since none of the repos is forked
            count_original_repos += total_repos
    return {
        'total_original_repos': count_original_repos,
        'total_forked_repos': count_forked_repos
    }


def repo_followers(github_response, bitbucket_response):
    """
    :param github_response: response from github
    :param bitbucket_response: response from bitbucket
    :return: int
    """
    total_watchers = 0
    if github_response is not None and github_response.status_code == 200:
        github_response_json = github_response.json()
        watchers = [repo['watchers_count'] for repo in github_response_json]
        total_watchers += sum(watchers)

    if bitbucket_response is not None and bitbucket_response.status_code == 200 \
        and bitbucket_response.json()['values']:
        # since all requests to bitbucket returns 200 OK we need to check if there are any repos too
        bitbucket_response_json = bitbucket_response.json()
        repo_watchers_urls = [repo['links']['watchers'] for repo in bitbucket_response_json['values']]
        repo_watchers_urls[:] = [url['href'] for url in repo_watchers_urls]
        watchers = []
        # start an event loop which runs till we get back the watchers
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        urls = repo_watchers_urls
        send_watchers_req = loop.run_until_complete(bitbucket_watchers(urls, loop))
        for res in send_watchers_req:
            try:
                if res.status_code == 200:
                    res_json = res.json()
                    # size is the key for watchers
                    watchers.append(res_json['size'])
            except:
                continue
        total_org_repos_watchers = sum(watchers)
        total_watchers += total_org_repos_watchers

    return total_watchers


def language_list(github_response, bitbucket_response):
    """
    reports the programing lanquages use in the repos
    :param github_response: response from github
    :param bitbucket_response: response from bitbucket
    :return: list
    """
    total_languages = []
    if github_response is not None and github_response.status_code == 200:
        github_response_json = github_response.json()
        languages = [repo['language'] for repo in github_response_json if repo['language'] is not None]
        list_count_languages = {'Github': [{language.lower(): languages.count(language)} for language in set(languages)]}
        total_languages.append(list_count_languages)

    if bitbucket_response is not None and bitbucket_response.status_code == 200\
            and bitbucket_response.json()['values']:
        bitbucket_response_json = bitbucket_response.json()
        bitbucket_languages = [repo['language'] for repo in bitbucket_response_json['values'] if repo['language'] is not None]
        list_count_bitbucket_languages = {'Bitbucket':[
            {language.lower(): bitbucket_languages.count(language)} for language in set(bitbucket_languages)]}
        total_languages.append(list_count_bitbucket_languages)

    return total_languages


def repo_topics(github_response):
    """
    reports repo topics for all public repos
    :param github_response: response from github
    :return: list of repo topics from github
    """
    repo_topics_count = []

    try:
        if github_response is not None and github_response.status_code == 200:
            github_response_json = github_response.json()
            repo_topics_count[:] = [repo['topics'] for repo in github_response_json]
    except:
        pass
    finally:
        return repo_topics_count


async def bitbucket_watcher(session, url):
    """
    an async method called to to use sessions to get data about a single url
    :param session: aiohttp ClientSession
    :param url: single watcher url
    :return: courotine
    """
    async with session.get(url, ssl=ssl.SSLContext()) as response:
        return await response.json()


async def bitbucket_watchers(urls, loop):
    """
    since each repo in bitbucket gives urls for the repo watchers
    we have to find an efficient ways to make calls to these urls
    :param urls: list of watcher urls
    :param loop: event loop
    :return: list of watchers
    """
    # Aiohttp recommends to use ClientSession as primary interface to make requests.
    # ClientSession allows you to store cookies between requests
    # and keeps objects that are common for all requests (event loop, connection and other things).
    async with aiohttp.ClientSession(loop=loop) as session:
        results = await asyncio.gather(*[bitbucket_watcher(session, url) for url in urls], return_exceptions=True)
        return results



