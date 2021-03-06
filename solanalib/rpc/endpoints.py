from enum import Enum


class Endpoint(str, Enum):
    DEFAULT = "https://api.google.mainnet-beta.solana.com"
    MAINNET_BETA = "https://api.mainnet-beta.solana.com"
    MAINNET_GOOGLE = "https://api.google.mainnet-beta.solana.com"
    GENESYS_GO = "https://ssc-dao.genesysgo.net"
    PROJECT_SERUM = "https://solana-api.projectserum.com"
    THE_INDEX = "https://rpc.theindex.io"

    @property
    def url(self) -> str:
        return self.value
