from enum import Enum
from typing import Protocol


class OperationType(Enum):
    synchronous = 'sync'
    asynchronous = 'async'


class MindboxOperation(Protocol):

    _name: str
    _type: OperationType

    def opeartion_body(self) -> dict:
        """Return dict with operation body"""
        raise NotImplementedError('Implement operation Body')

    def name(self) -> str:
        """Return operation name"""
        return self._name

    def opeartion_type(self) -> str:
        return self._type.value
