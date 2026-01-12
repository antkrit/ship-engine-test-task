from typing import Annotated

from fastapi import Header

from ..core.exceptions.http_exceptions import UnauthorizedException


async def get_api_key(api_key: Annotated[str | None, Header(alias="X-API-Key")] = None) -> str:
    if not api_key:
        raise UnauthorizedException("API key required. Please provide X-API-Key header.")
    
    # Allow all API keys for demonstration purposes
    return api_key
