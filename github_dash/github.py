import logging
import os

from exceptions import TokenNotFoundException

logger = logging.getLogger(__name__)

GITHUB_API_TOKEN = os.environ.get('GITHUB_API_TOKEN')

if GITHUB_API_TOKEN is None:
    logger.error('GitHub API Token Not Found')
    raise TokenNotFoundException
