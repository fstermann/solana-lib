from solanalib.util import SafeDict


class AccountInfo(SafeDict):
    @property
    def has_info(self):
        return self["result"]["value"] is not None

    @property
    def parsed(self) -> SafeDict:
        return self["result"]["value"]["data"]["parsed"]

    @property
    def info(self) -> SafeDict:
        return self.parsed["info"]

    @property
    def mint(self):
        return self.info["mint"]
