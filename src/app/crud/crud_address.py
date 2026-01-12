from fastcrud import FastCRUD

from ..models.address import Address
from ..schemas.address import (
    AddressCreateInternal,
    AddressDelete,
    AddressRead,
    AddressUpdate,
    AddressUpdateInternal,
)

CRUDAddress = FastCRUD[Address, AddressCreateInternal, AddressUpdate, AddressUpdateInternal, AddressDelete, AddressRead]
crud_addresses = CRUDAddress(Address)

