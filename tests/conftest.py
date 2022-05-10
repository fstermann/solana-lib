import json

import pytest

from solanalib.nft.nft_transaction import NftTransaction
from solanalib.parser import TransferTransaction


@pytest.fixture
def load_nft_tx():
    def loader(tx_type: str, tx_id: str, as_dict: bool = False) -> NftTransaction:
        with open(f"tests/nft/txs/{tx_type}/tx_{tx_type}_{tx_id}.json", "r") as f:
            data = json.load(f)
        if as_dict:
            return data["result"]
        tx = NftTransaction(transaction=data["result"])
        return tx

    return loader


@pytest.fixture
def load_transfer_tx():
    def loader(tx_type: str, tx_id: str, as_dict: bool = False) -> TransferTransaction:
        with open(f"tests/nft/txs/{tx_type}/tx_{tx_type}_{tx_id}.json", "r") as f:
            data = json.load(f)
        if as_dict:
            return data["result"]
        tx = TransferTransaction(transaction=data["result"])
        return tx

    return loader


@pytest.fixture
def load_account_info():
    def loader(tx_type: str, account: str) -> NftTransaction:
        with open(f"tests/nft/txs/{tx_type}/accountInfo_{account}.json", "r") as f:
            data = json.load(f)
        return data

    return loader
