import json

import pytest
from solanalib.nft.models import Transaction


@pytest.fixture
def load_tx():
    def loader(tx_type: str, tx_id: str, as_dict: bool = False) -> Transaction:
        with open(f"tests/nft/txs/{tx_type}/tx_{tx_type}_{tx_id}.json", "r") as f:
            data = json.load(f)
        if as_dict:
            return data["result"]
        tx = Transaction(transaction=data["result"])
        return tx

    return loader


@pytest.fixture
def load_account_info():
    def loader(tx_type: str, account: str) -> Transaction:
        with open(f"tests/nft/txs/{tx_type}/accountInfo_{account}.json", "r") as f:
            data = json.load(f)
        return data

    return loader
