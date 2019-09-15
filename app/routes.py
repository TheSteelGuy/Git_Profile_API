import logging

import flask
from flask import Response, jsonify
from .request_helper import handle_api_response
from app import github_root_url, bitbucket_root_url
app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)


@app.route("/<organization>", methods=["GET"])
def get_repos(organization):
    github_url = github_root_url+'orgs/'+organization + '/repos'
    bitbucket_url = bitbucket_root_url + 'repositories/' + organization
    result = handle_api_response(github_url=github_url, bitbucket_url=bitbucket_url)
    return jsonify({'result': result})
