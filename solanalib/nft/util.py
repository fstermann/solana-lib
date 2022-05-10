from typing import List

from .activities import Activity, ActivityType
from .nft_transaction import NftTransaction
from .parse import parse_transaction


def sort_activities(activities: List[Activity]) -> List[Activity]:
    # Sort out duplicates
    unique_activities = set(activities)

    # Sort by blocktime reverse
    sorted_activities = sorted(
        unique_activities, key=lambda x: x.block_time, reverse=True
    )
    return sorted_activities


def sort_transactions(transactions: List[NftTransaction]) -> List[NftTransaction]:
    # Sort out duplicates
    unique_transactions = set(transactions)

    # Sort by blocktime reverse
    sorted_transactions = sorted(
        unique_transactions, key=lambda x: x.block_time, reverse=True
    )
    return sorted_transactions


def get_previous_token_account(activities: List[Activity]):
    last_activity = activities[-1]

    if last_activity.type_ == ActivityType.MINT:

        return None
    return last_activity.old_token_account


def parse_all_transactions(transactions: List[NftTransaction]) -> List[Activity]:
    unique_transactions = sort_transactions(transactions)
    return [parse_transaction(transaction=tx) for tx in unique_transactions]
