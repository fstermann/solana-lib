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