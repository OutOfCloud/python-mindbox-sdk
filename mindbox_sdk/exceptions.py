from typing import Optional


class MindboxError(Exception):

    def __init__(self, message: Optional[str] = None,
                 status: Optional[str] = None,
                 status_code: Optional[int] = None,
                 error_id: Optional[str] = None,
                 ) -> None:
        super().__init__(message)
        self._status = status
        self._status_code = status_code
        self._message = message
        self._error_id = error_id

    def __str__(self):
        return f'STATUS:{self._status}|\
                 MESSAGE: {self._message}|\
                 CODE:{self._status_code}|\
                 ERROR_ID:{self._error_id}'


class MindboxConnectionError(MindboxError):
    pass


class MindboxProtocolError(MindboxError):
    pass


class MindboxValidationError(MindboxError):
    pass


class MindboxAlreadyProcessedError(MindboxError):
    pass
