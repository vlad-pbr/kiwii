from dataclasses import dataclass


@dataclass
class SSLCertChain:
    certfile: str
    keyfile: str
