"""
I'm Kiwii

I'm a fully fledged client-server IOT architecture, all in one python package. Some of my main features:
- Python 3 standard library only
- Cross-platform
- Dockerized
- Self-documented
- Built-in CLI and GUI clients
- Built-in server which strives to adhere to the best security practices

This package includes everything that is required to run a local server, interact with it and set up agent machines
which actually perform the IOT tasks. The idea is to run a server instance where it can be accessed externally
and connect your agent machines to this server which then query the server for current state in order to enforce
that state.

For example, you can connect your PC to the server in order to control it remotely (e.g. turn on music or
control home devices such as smart bulbs, external speakers, etc.). Kiwii allows you to do it easily once your
remote server is up.

My control over external devices can be extended by installing controller packages which reside in separate
repositories, but can be easily installed from pypi. I have some official controllers, but you can implement
your own one easily - it's a matter of writing some python code.

Documentation for my underlying architecture resides in docstrings stored in related submodules which can be
easily accessed by spinning up a local server and accessing the documentation endpoint (or via source code).
"""

from pathlib import Path

from kiwii.parser import parse

__version__ = "0.1.0"


def cli():
    """Entrypoint for kiwii command line interface which simply calls `parse` with parameters."""

    parse(Path(__file__).stem, __doc__, __version__)


if __name__ == "__main__":
    cli()
