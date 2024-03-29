# Author: Dina Hassanein (22066792)
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

    def get_id(self) -> str:
        """Get inventory item id."""
        return self._item_id

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

        check = Database.execute_and_fetchone("SELECT id from public.inventory\
                                               WHERE name = %s", name)
        if check is not None:
            raise AlreadyExistsError("An item with this name already exists.")

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

    def set_threshold(self, threshold: int) -> None:
        """
        Update the inventory items's threshold.

        :raises AuthorizationError: If active user does not have permission.
        """
        ActiveUser.get().raise_without_permission("inventory.update")

        Database.execute_and_commit(
            "UPDATE public.inventory SET threshold = %s WHERE id = %s",
            threshold, self._item_id)

    def add_quantity(self, quantity: int) -> None:
        """
        Increase the given quantity from the inventory items's quantity.

        :raises AuthorizationError: If active user does not have permission.
        """
        ActiveUser.get().raise_without_permission("inventory.update")

        Database.execute_and_commit(
            "UPDATE public.inventory SET quantity = quantity + %s \
            WHERE id = %s",
            quantity, self._item_id)

    def subtract_quantity(self, quantity: int) -> None:
        """
        Decrease the given quantity from the inventory items's quantity.

        :raises AuthorizationError: If active user does not have permission.
        :raises InputError: If given quantity is more than current quantity.
        """
        ActiveUser.get().raise_without_permission("inventory.update")

        item_quantity = self.get_quantity()
        if item_quantity < quantity:
            raise InputError(
                "Can't remove quantity more than current item\
                quantity (negative result)")

        Database.execute_and_commit(
            "UPDATE public.inventory SET quantity = quantity - %s \
            WHERE id = %s",
            quantity, self._item_id)

    def check_quantity_above_threshold(self) -> bool:
        """Check if the given item's quantity is above the threshold."""
        item_quantity = self.get_quantity()
        item_threshold = self.get_threshold()
        return item_quantity > item_threshold

    def delete(self):
        """
        Delete the inventory item record from the database.

        :raises AuthorizationError: If active user does not have permission.
        """
        ActiveUser.get().raise_without_permission("inventory.delete")

        Database.execute_and_commit(
            "DELETE FROM public.inventory WHERE id = %s",
            self._item_id)
