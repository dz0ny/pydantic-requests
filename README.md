[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/dz0ny/pydantic-requests.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/dz0ny/pydantic-requests/context:python)
[![PyPI](https://img.shields.io/pypi/dm/pydantic-requests.svg)](https://pypi.org/project/pydantic-requests/)


# Marriage of Pydantic and Requests

A helper that integrates Pydantic with requests library for seamless access to defined Models.

## Example

```python
from enum import Enum
from pydantic import BaseModel
from pydantic_requests import PydanticSession


class DNSStatus(Enum):
    """DNS OP response codes.
    ref: https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml#dns-parameters-6
    """

    # No Error = 0
    NoError = 0

    # Format Error = 1
    FormErr = 1

    # Server Failure
    ServFail = 2

    # Non-Existent Domain
    NXDomain = 3


class DNSQuery(BaseModel):
    Status: DNSStatus

    class Config:
        """Configure DNS query."""

        allow_mutation = False
        arbitrary_types_allowed = True


with PydanticSession(
    {200: DNSQuery}, headers={"accept": "application/dns-json"}
) as session:
    domain = "dz0ny.xyz"
    res = session.get(
        "https://cloudflare-dns.com/dns-query", params={"name": domain, "type": "NS"}
    )
    res.raise_for_status()
    query: DNSQuery = res.model
    if query.Status == DNSStatus.NXDomain:
        print("Domain is not registered.")
    else:
        print("Domain is registered.")

```
