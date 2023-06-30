from dataclasses import dataclass


@dataclass
class SSLCertChain:
    """
    `dataclass` wrapper around the parameters required by the `SSLContext`'s `load_cert_chain` method which
    are used as the TLS certificate location.
    """

    certfile: str
    keyfile: str
