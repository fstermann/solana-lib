from solanalib.rpc.parameter import Encoding, Commitment
import functools


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
    else:
        return decorator_payload(_func)


class MethodBuilder:
    @payload(method="getTransaction")
    def get_transaction(
        self,
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

    @payload(method="getTokenLargestAccounts")
    def get_token_largest_accounts(
        self,
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

    @payload(method="getSignaturesForAddress")
    def get_signatures_for_address(
        self,
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

    @payload(method="getAccountInfo")
    def get_account_info(
        self,
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
