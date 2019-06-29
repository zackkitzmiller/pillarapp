from flask import Flask, render_template, request

from exceptions import (
    OrginizationNotFoundException,
    OrginizationRequiredException
)
from github_client import client, STARS_SORT

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search')
def search():
    org = request.args.get('orginization', None)
    if org is None:
        raise OrginizationRequiredException

    try:
        org = client.get_organization(org)
    except: # TODO, Name this Exception
        raise OrginizationNotFoundException

    print org
    repos = org.get_repos()
    for repo in repos:
        print repo.stargazers_count

    return render_template('search.html')
