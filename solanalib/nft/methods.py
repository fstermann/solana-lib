from typing import List

from solanalib.logger import logger
from solanalib.nft.models import Activity, ActivityType, NFTTransaction
from solanalib.nft.parse import parse_transaction
from solanalib.publickey import PublicKey
from solanalib.rpc.client import Client
from solanalib.rpc.proclient import ProClient


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


def get_mint_activities(
    token_mint: PublicKey, client: ProClient = ProClient()
) -> List[Activity]:
    current_token_account = get_current_token_account(
        token_mint=token_mint, client=client
    )
    all_activities = []

    while current_token_account:
        logger.debug(
            f"Fetching all activites for token account {current_token_account}"
        )
        activities = get_mint_activites_for_token_account(
            token_mint=token_mint, token_account=current_token_account, client=client
        )
        all_activities += activities

        last_activity = activities[-1]
        if last_activity.type_ != ActivityType.MINT:
            current_token_account = last_activity.old_token_account
        else:
            logger.debug(
                f"Found all activites for token account {current_token_account}"
            )
            current_token_account = None

    return all_activities


def get_mint_activites_for_token_account(
    token_mint: str, token_account: str, client: ProClient = ProClient()
) -> List[Activity]:
    transactions = client.get_all_parsed_transactions_for_address(account=token_account)
    txs = [
        NFTTransaction(mint=token_mint, transaction=tx["result"]) for tx in transactions
    ]
    activities = parse_all_transactions(transactions=txs)
    return activities


def get_current_token_account(token_mint: PublicKey, client: Client = Client()):
    response = client.get_token_largest_accounts(token_mint=token_mint)
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
