"""
API routes which are always registered when initializing the API.
"""

from .favicon import favicon

from .status import status

from .agent_status import agent_status
from .agent import agent_post
