import requests

from .exceptions import (MindboxAlreadyProcessedError,
                            MindboxConnectionError, MindboxProtocolError,
                            MindboxValidationError)
from .operation import MindboxOperation, OperationType
from .response import MindboxResponse
from .shared_types import ApiKey, DeviceUUID, Endpoint


class Mindbox:

    _endpoint: Endpoint
    _api_key: ApiKey

    def __init__(self, endpoint: Endpoint, api_key: ApiKey):
        self._endpoint = endpoint
        self._api_key = api_key

    def request(self, mb_operation: MindboxOperation) -> MindboxResponse:
        json_reponse = self._request_process(
            operation_name=mb_operation.name(),
            device_uuid=mb_operation.device_uuid(),
            operation_body=mb_operation.opeartion_body(),
            request_type=mb_operation.opeartion_type(),
        )
        return MindboxResponse(**json_reponse)

    def _url(self, request_type) -> str:
        return f'https://api.mindbox.ru/v3/operations/{request_type}/'

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
