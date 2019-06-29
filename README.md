# Github Dashboard

## Requirements

It's recommended that you use a virtual env to run this application.

`pip install -r requirements.txt`

The server also requires redis. To install on a mac

`brew install redis`

To start Redis:

`redis-server`

The server is built with Flask. To run the server:

1. copy .env.sample to .env and enter your GitHub Token, development environment, and host for Redis
2. run `EXPORT FLASK_APP=github_dash/server.py`
3. run `source .env && flask run`
