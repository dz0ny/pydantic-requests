import typing as t

import pytest
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError

from pydantic_requests import PydanticResponse, PydanticSession


class Foo(BaseModel):
    foo: t.Any


def test_valid_parser_and_model(cov):
    """Ensure parsing and model logic work."""
    res = PydanticResponse(PydanticSession({200: Foo}))
    res.status_code = 200
    res._content = b'{"foo": "bar"}'
    assert res.model


def test_invalid_model(cov):
    """Ensure that proper exception bubbles up."""
    res = PydanticResponse(PydanticSession({200: Foo}))
    res.status_code = 200
    res._content = b'{"bar": "foo"}'
    with pytest.raises(ValidationError) as exc:
        res.model
    exc.match("type=value_error.missing")
