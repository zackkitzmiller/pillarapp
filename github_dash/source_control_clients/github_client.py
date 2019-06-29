import logging
import os
import sys

from ..exceptions import (
    InvalidSortException,
    OrginizationNotFoundException,
    TokenNotFoundException
)

use_cache = False
try:
    from ..cache import client as cache_client
    use_cache = True
except ImportError:
    pass

from github import Github


logger = logging.getLogger(__name__)
logging.basicConfig()

CACHE_TTL = 24 * 60 * 60
GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN')
DEFAULT_SORT = STARS_SORT = "stars"
FORKS_SORT = "forks"
CONTRIBUTORS_SORT = "contributors"
VALID_SORTS = frozenset((DEFAULT_SORT, FORKS_SORT, CONTRIBUTORS_SORT))

if GITHUB_API_TOKEN is None:
    logger.error('GitHub API Token Not Found')
    raise TokenNotFoundException

_client = Github(GITHUB_API_TOKEN)


def get_sorted_repos(orginization, sort=DEFAULT_SORT):
    try:
        org = _client.get_organization(orginization)
    except Exception:
        raise OrginizationNotFoundException

    if sort is None:
        sort = DEFAULT_SORT

    if sort not in VALID_SORTS:
        raise InvalidSortException

    # Sorting doesn't work w/ this client, we're going to have to do it
    # in memory, learned this too late in the game to choose a different client
    # or write my own. RIP
    _repos = []
    repos = org.get_repos(type='sources')
    for repo in repos:
        _repos.append({
            'name': repo.name,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'contributors': get_contributor_count(repo)
        })

    return sorted(_repos, key=lambda x: x[sort], reverse=True)


# little helper here, because we get a generator back from repo.get_contributors
def get_contributor_count(repo):

    # probably a cleaner way to make redis optional, but in time crunch
    # this is really really slow.
    if use_cache:
        # This block could be abstracted into it's own method to
        # reduce cyclomatic complexty a little bit, but I'm running short
        # on time
        cached_count = cache_client.get(_cache_key(repo.name))
        logger.info("looking in cache {0}".format(repo.name))
        if cached_count:
            logger.info('cache hit {0}'.format(repo.name))
            return int(cached_count)

        logger.info('cache miss {0}'.format(repo.name))

    contributor_count = 0
    try:
        contributors = repo.get_stats_contributors()
    except Exception: # todo name
        return contributor_count

    if contributors is not None:
        for contributor in contributors:
            contributor_count += 1
            # Hack - short circuit at 15. This endpoint is incredibly slow.
            # I don't have a good solution for this yet.
            if contributor_count >= 15:
                break

    if use_cache:
        _key = _cache_key(repo.name)
        cache_client.setex(_key, CACHE_TTL, int(contributor_count))
    return int(contributor_count)


def _cache_key(repo_name):
    return "{0}:contributor_count".format(repo_name)
