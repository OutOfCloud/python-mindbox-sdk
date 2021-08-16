class MindboxResponse:

    _status: str
    _body: dict = {}

    def __init__(self, **kwargs):

        self._status = kwargs.pop('status')
        self._body = kwargs

    def status(self):
        return self._status

    def content(self):
        return self._body


