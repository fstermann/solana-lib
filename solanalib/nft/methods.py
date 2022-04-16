from typing import List

from solanalib.logger import logger
from solanalib.nft.models import Activity, NFTTransaction
from solanalib.nft.parse import parse_transaction
from solanalib.publickey import PublicKey
from solanalib.rpc.client import Client


def get_collection_activities(creator_address):
    # get mint list

    # for mint in mint list
    #   get largest token account
    #   get all transactions for current token account *
    #   for tx in txs
    #       parse transaction to get activity type
    #       if last tx is transfer
    #           repeat from *
    pass


def get_current_token_account(tokent_mint: PublicKey, client: Client = Client()):
    response = client.get_token_largest_accounts(token_mint=tokent_mint)
    account_infos = response["result"]["value"]
    largest_account = [
        info["address"] for info in account_infos if info["amount"] == "1"
    ]
    if len(largest_account) == 1:
        return largest_account[0]
    if len(largest_account) > 1:
        msg = "Got more than one account for mint."
        logger.error(msg)
        raise ValueError(msg)
    if len(largest_account) < 1:
        msg = "Found no account for mint."
        logger.error(msg)
        raise ValueError(msg)


def parse_all_transactions(transactions: List[NFTTransaction]) -> List[Activity]:
    activities = [parse_transaction(transaction=tx) for tx in transactions]
    return activities
