from flask import Flask, render_template, request

from exceptions import (
    OrginizationRequiredException
)
from source_control_clients import github_client

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')


@app.route('/search')
def search():
    org = request.args.get('orginization', None)
    if org is None:
        raise OrginizationRequiredException

    sort_choice = request.args.get('sort', github_client.DEFAULT_SORT)
    repos = github_client.get_sorted_repos(org, sort=sort_choice)

    return render_template('search.html', repos=repos, orginization=org)
