from typing import List, Union

import requests

from .endpoints import Endpoint
from .methods import MethodBuilder
from .parameter import Commitment, Encoding


class Client:
    endpoint: Union[Endpoint, str] = Endpoint.DEFAULT
    method_builder: MethodBuilder = None

    def __init__(self, endpoint: Union[Endpoint, str] = Endpoint.DEFAULT):
        self.endpoint = endpoint
        self.method_builder = MethodBuilder()

    def _make_request(self, payload):
        response = requests.post(self.endpoint.url, json=payload)
        return response.json()

    def health_check(self):
        pass

    def get_transaction(
        self,
        transaction_signature: str,
        encoding: Encoding = Encoding.JSON_PARSED,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        payload = self.method_builder.get_transaction(
            transaction_signature=transaction_signature,
            encoding=encoding,
            commitment=commitment,
        )
        return self._make_request(payload)

    def get_transactions(
        self,
        transaction_signatures: List[str],
        encoding: Encoding = Encoding.JSON_PARSED,
        commitment: Commitment = Commitment.FINALIZED,
    ):
        payload = [
            self.method_builder.get_transaction(
                transaction_signature=transaction_signature,
                encoding=encoding,
                commitment=commitment,
            )
            for transaction_signature in transaction_signatures
        ]
        return self._make_request(payload)
