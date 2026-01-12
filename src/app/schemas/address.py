from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class AddressPartial(BaseModel):
    """Partial address information that may already be known."""
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(default=None, max_length=100, examples=["John Doe"])] = None
    company: Annotated[str | None, Field(default=None, max_length=100, examples=["Acme Inc."])] = None
    phone: Annotated[str | None, Field(default=None, max_length=20, examples=["+1-555-123-4567"])] = None
    address_line1: Annotated[str | None, Field(default=None, max_length=200, examples=["123 Main St"])] = None
    address_line2: Annotated[str | None, Field(default=None, max_length=200, examples=["Apt 4B"])] = None
    address_line3: Annotated[str | None, Field(default=None, max_length=200)] = None
    city_locality: Annotated[str | None, Field(default=None, max_length=100, examples=["Austin"])] = None
    state_province: Annotated[str | None, Field(default=None, max_length=50, examples=["TX"])] = None
    postal_code: Annotated[str | None, Field(default=None, max_length=20, examples=["78701"])] = None
    country_code: Annotated[str | None, Field(default=None, max_length=2, examples=["US"])] = None


class AddressRecognizeRequest(BaseModel):
    """Request schema for address recognition."""
    model_config = ConfigDict(extra="forbid")

    text: Annotated[str, Field(min_length=1, max_length=5000, examples=["John Doe\n123 Main St\nAustin, TX 78701"])]
    address: Annotated[AddressPartial | None, Field(default=None)] = None


class AddressRecognizeResponse(BaseModel):
    """Response schema for address recognition."""
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(default=None, examples=["John Doe"])] = None
    company: Annotated[str | None, Field(default=None, examples=["Acme Inc."])] = None
    phone: Annotated[str | None, Field(default=None, examples=["+1-555-123-4567"])] = None
    address_line1: Annotated[str | None, Field(default=None, examples=["123 Main St"])] = None
    address_line2: Annotated[str | None, Field(default=None, examples=["Apt 4B"])] = None
    address_line3: Annotated[str | None, Field(default=None)] = None
    city_locality: Annotated[str | None, Field(default=None, examples=["Austin"])] = None
    state_province: Annotated[str | None, Field(default=None, examples=["TX"])] = None
    postal_code: Annotated[str | None, Field(default=None, examples=["78701"])] = None
    country_code: Annotated[str | None, Field(default=None, examples=["US"])] = None


class AddressBase(BaseModel):
    """Base schema with common address fields."""
    name: Annotated[str | None, Field(default=None, max_length=100, examples=["John Doe"])] = None
    company: Annotated[str | None, Field(default=None, max_length=100, examples=["Acme Inc."])] = None
    phone: Annotated[str | None, Field(default=None, max_length=20, examples=["+1-555-123-4567"])] = None
    address_line1: Annotated[str | None, Field(default=None, max_length=200, examples=["123 Main St"])] = None
    address_line2: Annotated[str | None, Field(default=None, max_length=200, examples=["Apt 4B"])] = None
    address_line3: Annotated[str | None, Field(default=None, max_length=200)] = None
    city_locality: Annotated[str | None, Field(default=None, max_length=100, examples=["Austin"])] = None
    state_province: Annotated[str | None, Field(default=None, max_length=50, examples=["TX"])] = None
    postal_code: Annotated[str | None, Field(default=None, max_length=20, examples=["78701"])] = None
    country_code: Annotated[str | None, Field(default=None, max_length=2, examples=["US"])] = None


class AddressCreate(AddressBase):
    """Schema for creating a new address."""
    model_config = ConfigDict(extra="forbid")


class AddressRead(TimestampSchema, AddressBase, UUIDSchema, PersistentDeletion):
    """Schema for reading address data."""
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class AddressUpdate(BaseModel):
    """Schema for updating an address (all fields optional)."""
    model_config = ConfigDict(extra="forbid")
    
    name: Annotated[str | None, Field(default=None, max_length=100, examples=["John Doe"])] = None
    company: Annotated[str | None, Field(default=None, max_length=100, examples=["Acme Inc."])] = None
    phone: Annotated[str | None, Field(default=None, max_length=20, examples=["+1-555-123-4567"])] = None
    address_line1: Annotated[str | None, Field(default=None, max_length=200, examples=["123 Main St"])] = None
    address_line2: Annotated[str | None, Field(default=None, max_length=200, examples=["Apt 4B"])] = None
    address_line3: Annotated[str | None, Field(default=None, max_length=200)] = None
    city_locality: Annotated[str | None, Field(default=None, max_length=100, examples=["Austin"])] = None
    state_province: Annotated[str | None, Field(default=None, max_length=50, examples=["TX"])] = None
    postal_code: Annotated[str | None, Field(default=None, max_length=20, examples=["78701"])] = None
    country_code: Annotated[str | None, Field(default=None, max_length=2, examples=["US"])] = None


class AddressCreateInternal(AddressBase):
    """Internal schema for address creation."""
    pass


class AddressUpdateInternal(AddressUpdate):
    """Internal schema for address updates."""
    updated_at: datetime


class AddressDelete(BaseModel):
    """Schema for soft deleting an address."""
    model_config = ConfigDict(extra="forbid")
    
    is_deleted: bool
    deleted_at: datetime

