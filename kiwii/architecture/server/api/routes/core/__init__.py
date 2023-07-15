"""
API routes which are always registered when initializing the API.
"""

from .favicon import favicon

from .status import status

from .agent import agent_post, agent_status
