import logging
import os

from exceptions import TokenNotFoundException

from github import Github

logger = logging.getLogger(__name__)
logging.basicConfig()

GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN')
STARS_SORT = "stars"
FORKS_SORT = "forks"


if GITHUB_API_TOKEN is None:
    logger.error('GitHub API Token Not Found')
    raise TokenNotFoundException

client = Github(GITHUB_API_TOKEN)
