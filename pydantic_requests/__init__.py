"""Response hook for pydantic and requests."""

from __future__ import annotations

import typing as t

import requests
from pydantic import BaseModel


class PydanticResponse(requests.Response):
    """An pydantic-enabled :class:`requests.Response <requests.Response>` object.
    Effectively the same, but with an intelligent ``.html`` property added.
    """

    def __init__(self, session: PydanticSession):
        super(PydanticResponse, self).__init__()
        self._object: t.Type[BaseModel] = None
        self.session = session

    @property
    def model(self) -> t.Type[BaseModel]:
        if not self._object:
            try:
                self._object = self.session.handlers[self.status_code](**self.json())
            except ValueError:
                raise ValueError(
                    f"Parser for status code {self.status_code} is missing in session."
                )
        return self._object

    @classmethod
    def _from_response(cls, response, session: PydanticSession):
        html_r = cls(session=session)
        html_r.__dict__.update(response.__dict__)
        return html_r


class PydanticSession(requests.Session):
    """ A consumable session, for cookie persistence and connection pooling,
    amongst other things.
    """

    def __init__(self, handlers: t.Dict[int, t.Type[BaseModel]], headers: dict = None):
        super().__init__()
        self.handlers = handlers
        self.hooks["response"].append(self.response_hook)
        if headers:
            self.headers.update(headers)

    def response_hook(self, response, **kwargs) -> PydanticResponse:
        """ Replace response by PydanticResponse. """
        return PydanticResponse._from_response(response, self)
