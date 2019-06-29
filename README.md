# Github Dashboard

## Requirements

It's recommended that you use a virtual env to run this application.

`pip install -r requirements.txt`

The server also will utilize redis if it's available.

`brew install redis`

To start Redis:

`redis-server`

The server is built with Flask. To run the server:

1. copy .env.sample to .env and enter your GitHub Token, development environment, and host for Redis
2. run `EXPORT FLASK_APP=github_dash/server.py`
3. run `source .env && flask run`

## Limitations
- [ ] Sorting in Memory. I went down the wrong route of using a Github API client that doesn't retun the results exactly like as I'd like. The README says it supports sorting, but it actually just doesn't work. I would have written my own, but alas, too late.
- [ ] Web requests to GitHub are syncronous
- [ ] The contributors count is inaccurate because of the Github API client (It names N*M requests where N is number of repos and M is number of contributors to that repo)
- [ ] Redis cache is used for speeding up testing/development. It's a premature optimization for sure
- [ ] Error handling is subpar. Need to write a handler to turn the psudo-generic 500s into 4XX with relevant user information