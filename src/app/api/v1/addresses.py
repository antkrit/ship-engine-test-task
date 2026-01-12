import re
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request
from fastcrud import PaginatedListResponse, compute_offset, paginated_response
from spacy import Language
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import get_spacy_model
from ...core.security import get_api_key
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import NotFoundException
from ...crud.crud_address import crud_addresses
from ...schemas.address import (
    AddressCreate,
    AddressRecognizeRequest,
    AddressRecognizeResponse,
    AddressRead,
    AddressUpdate,
)

router = APIRouter(prefix="/addresses", tags=["addresses"])


def parse_address(text: str, nlp_model: Language, known_address: dict[str, Any] | None = None) -> AddressRecognizeResponse:
    result: dict[str, Any] = {}
    if known_address:
        result = {k: v for k, v in known_address.items() if v is not None}

    text = text.strip()
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    if not lines:
        return AddressRecognizeResponse(**result)

    doc = nlp_model(text)

    for ent in doc.ents:
        if ent.label_ == "PERSON" and "name" not in result:
            result["name"] = ent.text.strip()
        elif ent.label_ == "ORG" and "company" not in result:
            result["company"] = ent.text.strip()
        elif ent.label_ == "GPE":
            ent_text = ent.text.strip()
            if "city_locality" not in result and len(ent_text.split()) == 1:
                result["city_locality"] = ent_text

    return AddressRecognizeResponse(**result)


@router.put("/recognize", response_model=AddressRecognizeResponse)
async def recognize_address(
    request: Request,
    address_data: AddressRecognizeRequest,
    api_key: Annotated[str, Depends(get_api_key)],
    nlp_model: Annotated[Language, Depends(get_spacy_model)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> AddressRecognizeResponse:
    """Recognize and parse address from unstructured text using spaCy.
    
    This endpoint extracts structured address data from unstructured text,
    including recipient name, address lines, city, state, postal code, and country.
    Uses spaCy NLP model for improved entity recognition and parsing.
    """
    known_address_dict = None
    if address_data.address:
        known_address_dict = address_data.address.model_dump(exclude_none=True)
    
    parsed_address = parse_address(address_data.text, nlp_model, known_address_dict)
    
    return parsed_address


@router.post("/", response_model=AddressRead, status_code=201)
async def create_address(
    request: Request,
    address_data: AddressCreate,
    api_key: Annotated[str, Depends(get_api_key)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> AddressRead:
    """Create a new address"""
    created_address = await crud_addresses.create(db=db, object=address_data, schema_to_select=AddressRead)
    if created_address is None:
        raise HTTPException(status_code=500, detail="Failed to create address")
    return created_address


@router.get("/", response_model=PaginatedListResponse[AddressRead])
async def list_addresses(
    request: Request,
    api_key: Annotated[str, Depends(get_api_key)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict[str, Any]:
    """List addresses with pagination"""
    addresses_data = await crud_addresses.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        is_deleted=False,
        schema_to_select=AddressRead,
    )
    
    response: dict[str, Any] = paginated_response(crud_data=addresses_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/{address_id}", response_model=AddressRead)
async def get_address(
    request: Request,
    address_id: str,
    _: Annotated[str, Depends(get_api_key)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> AddressRead:
    """Get an address by uuid"""
    address = await crud_addresses.get(db=db, uuid=address_id, is_deleted=False, schema_to_select=AddressRead)
    if address is None:
        raise NotFoundException("Address not found")
    return address


@router.patch("/{address_id}", response_model=AddressRead)
async def update_address(
    request: Request,
    address_id: str,
    address_data: AddressUpdate,
    _: Annotated[str, Depends(get_api_key)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> AddressRead:
    """Update an address"""
    address = await crud_addresses.get(db=db, uuid=address_id, is_deleted=False)
    if address is None:
        raise NotFoundException("Address not found")
    
    updated_address = await crud_addresses.update(
        db=db, object=address_data, id=address_id, schema_to_select=AddressRead
    )
    return updated_address


@router.delete("/{address_id}", response_model=dict[str, str])
async def delete_address(
    request: Request,
    address_id: str,
    _: Annotated[str, Depends(get_api_key)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    """Soft delete an address"""
    address = await crud_addresses.get(db=db, uuid=address_id, is_deleted=False)
    if address is None:
        raise NotFoundException("Address not found")
    
    await crud_addresses.delete(db=db, id=address_id)
    return {"message": "Address deleted"}

