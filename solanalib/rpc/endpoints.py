from enum import Enum


class Endpoint(Enum):
    DEFAULT = "https://rpc.theindex.io"
    MAINNET_BETA = "https://api.mainnet-beta.solana.com"
    GENESYS_GO = "https://ssc-dao.genesysgo.net"
    PROJECT_SERUM = "https://solana-api.projectserum.com"
    THE_INDEX = "https://rpc.theindex.io"

    @property
    def url(self):
        return self.value
