import functools

from solanalib.rpc.parameter import Commitment, Encoding, TransactionDetails


def payload(_func=None, *, method: str, id_: int = 1):
    def decorator_payload(func):
        @functools.wraps(func)
        def wrapper_payload(*args, **kwargs):
            params = func(*args, **kwargs)
            return {
                "jsonrpc": "2.0",
                "id": id_,
                "method": method,
                "params": params,
            }

        return wrapper_payload

    if _func is None:
        return decorator_payload
    return decorator_payload(_func)


class MethodBuilder:
    @staticmethod
    @payload(method="getTransaction")
    def get_transaction(
        transaction_signature: str,
        encoding: Encoding = Encoding.JSON_PARSED,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        params = [
            transaction_signature,
            {
                "encoding": encoding.value,
                "commitment": commitment.value,
            },
        ]
        return params

    @staticmethod
    @payload(method="getTokenLargestAccounts")
    def get_token_largest_accounts(
        token_mint: str,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        params = [
            token_mint,
            {
                "commitment": commitment.value,
            },
        ]
        return params

    @staticmethod
    @payload(method="getSignaturesForAddress")
    def get_signatures_for_address(
        account: str,
        limit: int = 1000,  # between 1 and 1000
        before: str = None,
        until: str = None,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        method_filter = {
            "commitment": commitment.value,
            "limit": limit,
        }
        if before:
            method_filter["before"] = before
        if until:
            method_filter["until"] = until

        params = [
            account,
            method_filter,
        ]
        return params

    @staticmethod
    @payload(method="getAccountInfo")
    def get_account_info(
        account: str,
        encoding: Encoding = Encoding.JSON_PARSED,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        params = [
            account,
            {
                "encoding": encoding.value,
                "commitment": commitment.value,
            },
        ]
        return params

    @staticmethod
    @payload(method="getBlock")
    def get_block(
        slot: int,
        encoding: Encoding = Encoding.JSON_PARSED,
        transaction_details: TransactionDetails = TransactionDetails.FULL,
        rewards: bool = True,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        params = [
            slot,
            {
                "encoding": encoding.value,
                "transaction_details": transaction_details.value,
                "rewards": rewards,
                "commitment": commitment.value,
            },
        ]
        return params
