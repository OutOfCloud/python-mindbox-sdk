import requests

from ._exceptions import (MindboxAlreadyProcessedError,
                          MindboxConnectionError, MindboxProtocolError,
                          MindboxValidationError)
from .operation import MindboxOperation, OperationType
from ._response import MindboxResponse
from ._types import ApiKey, DeviceUUID, Endpoint
from ._transport_protocol import MindboxTransport


class Mindbox(MindboxTransport):

    _endpoint: Endpoint
    _api_key: ApiKey

    def __init__(self, endpoint: Endpoint, api_key: ApiKey):
        self._endpoint = endpoint
        self._api_key = api_key

    def request(self, mb_operation: MindboxOperation) -> MindboxResponse:
        json_response = self._request_process(
            operation_name=mb_operation.name(),
            device_uuid=mb_operation.device_uuid(),
            operation_body=mb_operation.operation_body(),
            request_type=mb_operation.operation_type(),
        )

        return MindboxResponse(**json_response)

    def _url(self, request_type) -> str:
        return f'https://api.mindbox.ru/v3/operations/{request_type}/'

    def _headers(self):
        return {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
            "Authorization": f'Mindbox secretKey="{self._api_key}"',
        }

    def _validate_response(self, mindbox_response: requests.Response) -> dict:

        mindbox_response_json = mindbox_response.json()
        mindbox_response_status = mindbox_response_json.get(
            'status',
            'InternalError'
        )

        if mindbox_response.status_code != requests.codes.ok:
            raise MindboxProtocolError(
                message=mindbox_response_json.get('errorMessage'),
                status_code=mindbox_response.status_code,
                status=mindbox_response_status,
                error_id=mindbox_response_json.get('errorId'),
            )
        if mindbox_response_status == 'ValidationError':

            messages = []
            for msg in mindbox_response_json.get('validationMessages', []):
                item_msg = f'VALID_MESSAGE:{msg.get("message")}\
                    LOCATION:{msg.get("location")}'
                messages.append(
                    item_msg,
                )
            raise MindboxValidationError(
                message='.'.join(messages),
                status_code=mindbox_response.status_code,
                status=mindbox_response_status,
                error_id=mindbox_response_json.get('errorId'),
            )
        if mindbox_response_status == 'TransactionAlreadyProcessed':
            raise MindboxAlreadyProcessedError()

        return mindbox_response_json

    def _request_process(self,
                         operation_name: str,
                         device_uuid: DeviceUUID,
                         operation_body: dict,
                         request_type: OperationType,
                         ) -> dict:

        url_params = {
            'endpointId': self._endpoint,
            'operation': operation_name,
            'deviceUUID': device_uuid,
        }

        try:
            mindbox_response = requests.post(
                url=self._url(request_type.name), params=url_params, json=operation_body)
        except requests.exceptions.RequestException as e:
            raise MindboxConnectionError from e

        return self._validate_response(mindbox_response)


class MindboxFake(Mindbox):

    def _request_process(*args, **kwargs) -> dict:
        # TODO FakeResponse and log.debug inputs
        print(kwargs)
        return {'status': 'Success'}
