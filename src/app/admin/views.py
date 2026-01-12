from typing import Annotated

from crudadmin import CRUDAdmin
from ..models.address import Address
from ..schemas.address import AddressCreate, AddressUpdate

def register_admin_views(admin: CRUDAdmin) -> None:
    """Register all models and their schemas with the admin interface.

    This function adds all available models to the admin interface with appropriate
    schemas and permissions.
    """
    admin.add_view(
        model=Address,
        create_schema=AddressCreate,
        update_schema=AddressUpdate,
        allowed_actions={"view", "create", "update", "delete"},
    )
