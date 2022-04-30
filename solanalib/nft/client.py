from typing import List

from solanalib.logger import logger
from solanalib.publickey import PublicKey
from solanalib.rpc.proclient import ProClient

from .activities import Activity
from .transaction import NFTTransaction
from .util import get_previous_token_account, parse_all_transactions, sort_activities


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


class NftClient:
    def __init__(self, client: ProClient = ProClient()):
        self.client = client

    def get_multiple_mint_activites(self, token_mints: List[str]) -> List[Activity]:
        return {mint: self.get_mint_activities(mint) for mint in token_mints}

    def get_mint_activities(self, token_mint: PublicKey) -> List[Activity]:
        logger.info(f"Fetching current token account for mint {token_mint}")
        current_token_account = self.get_current_token_account(token_mint=token_mint)

        logger.info(f"Fetching all activities for mint {token_mint}")
        all_activities = []

        while current_token_account:
            logger.debug(
                f"Fetching all activites for token account {current_token_account}"
            )
            activities = self.get_mint_activites_for_token_account(
                token_mint=token_mint,
                token_account=current_token_account,
            )
            all_activities += activities

            logger.debug(
                f"Found all activites for token account {current_token_account}"
            )
            current_token_account = get_previous_token_account(activities=activities)

        logger.info(f"Found all activities for mint {token_mint}")
        sorted_activities = sort_activities(all_activities)
        return sorted_activities

    def get_mint_activites_for_token_account(
        self, token_mint: str, token_account: str
    ) -> List[Activity]:
        transactions = self.client.get_all_parsed_transactions_for_address(
            account=token_account
        )
        txs = [
            NFTTransaction(mint=token_mint, transaction=tx["result"])
            for tx in transactions
            if not tx["result"]["meta"]["err"]
        ]
        activities = parse_all_transactions(transactions=txs)
        return activities

    def get_current_token_account(self, token_mint: PublicKey):
        response = self.client.get_token_largest_accounts(token_mint=token_mint)
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
