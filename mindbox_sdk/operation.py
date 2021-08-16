from enum import Enum
from typing import Protocol

from ._response import MindboxResponse
from ._transport_protocol import MindboxTransport
from ._types import DeviceUUID, OperationName


class OperationType(Enum):
    synchronous = 'sync'
    asynchronous = 'async'


class MindboxOperation(Protocol):

    _name: OperationName
    _type: OperationType
    _api_transport: MindboxTransport

    def operation_body(self) -> dict:
        """Return dict with operation body"""
        raise NotImplementedError('Implement operation Body')

    def name(self) -> str:
        """Return operation name"""
        return self._name

    def operation_type(self) -> str:
        return self._type.value

    def device_uuid(self) -> DeviceUUID:
        return ''

    def execute(self, *args, **kwargs) -> MindboxResponse:
        return self._process_operation()

    def __call__(self) -> MindboxResponse:
        return self._process_operation()

    def _process_operation(self):
        return self._api_transport.request(mb_operation=self)
