from typing import Protocol


class MindboxTransport(Protocol):

    def request(self):
        raise NotImplementedError()


class MindboxAsyncTransport(Protocol):

    async def request(self):
        raise NotImplementedError()
