"""
`argparse` parser for the top level kiwii CLI.

Parser architecture in kiwii is straightforward:
- top level parser reads args it knows using `parse_known_args`
- it then semantically validates the arguments making sure they make sense
- in case semantics check out, parser performs the requested actions
- if lower level parser is requested, the top level parser calls the lower level subparser, providing it with all
  the unknown arguments which were left from `parse_known_args` call
"""

from .parser import parse
