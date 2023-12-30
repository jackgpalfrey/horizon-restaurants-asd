"""Module for handling specific inventories."""
from ..utils.Database import Database
from ..user.ActiveUser import ActiveUser
from src.utils.errors import AlreadyExistsError, InputError
from .utils import validate_item_name


class InventoryItem:
    """Class to manage a specific reservation."""

    def __init__(self, item_id: str):
        """Don't call outside of BranchInventory."""
        self._item_id = item_id

    def get_name(self) -> str:
        """Get inventory item's name."""
        result = Database.execute_and_fetchone(
            "SELECT name FROM public.inventory WHERE id = %s",
            self._item_id)

        assert result is not None
        return result[0]

    def get_quantity(self) -> int:
        """Get inventory item's quantity."""
        result = Database.execute_and_fetchone(
            "SELECT quantity FROM public.inventory WHERE id = %s",
            self._item_id)

        assert result is not None
        return result[0]

    def get_threshold(self) -> int:
        """Get inventory item's threshold."""
        result = Database.execute_and_fetchone(
            "SELECT threshold FROM public.inventory WHERE id = %s",
            self._item_id)

        assert result is not None
        return result[0]

    def set_name(self, name: str) -> None:
        """
        Update the inventory items's name.

        :raises AuthorizationError: If active user does not have permission.
        :raises InputError: If item name given is invalid.
        """
        ActiveUser.get().raise_without_permission("inventory.update")

        if not validate_item_name(name):
            raise InputError("Invalid item name.")

        Database.execute_and_commit(
            "UPDATE public.inventory SET name = %s WHERE id = %s",
            name, self._item_id)

    def set_quantity(self, quantity: int) -> None:
        """
        Update the inventory items's quantity.

        :raises AuthorizationError: If active user does not have permission.
        """
        ActiveUser.get().raise_without_permission("inventory.update")

        Database.execute_and_commit(
            "UPDATE public.inventory SET quantity = %s WHERE id = %s",
            quantity, self._item_id)
