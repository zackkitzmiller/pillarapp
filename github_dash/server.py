from flask import Flask, render_template, request

from exceptions import (
    OrginizationRequiredException,
    OrginizationNotFoundException
)

from source_control_clients import github_client

# Here we could add our telemetry, centralized exception handling, etc.
# We don't need that for this purpose, but I wanted to note regardless
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/search')
def search():
    org = request.args.get('orginization', None)
    if org is None:
        raise OrginizationRequiredException

    sort_choice = request.args.get('sort', None)
    try:
        repos = github_client.get_sorted_repos(org, sort=sort_choice)
    except OrginizationNotFoundException:
        repos = None

    return render_template('search.html', repos=repos, orginization=org)
