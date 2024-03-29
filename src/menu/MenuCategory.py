# Author: Jack Palfrey (22032928)
"""Module for managing menu categories."""
from src.menu.utils import validate_menu_name
from src.user.ActiveUser import ActiveUser
from src.utils.errors import InputError
from ..utils.Database import Database


class MenuCategory:
    """Class for managing a specific category."""

    def __init__(self, category_id: str):
        """Don't call outside of BranchMenu."""
        self._category_id = category_id

    def get_id(self) -> str:
        """Get ID of category."""
        return self._category_id

    def get_name(self) -> str | None:
        """Get the categories name."""
        sql = "SELECT name FROM public.menucategory WHERE id=%s;"
        result = Database.execute_and_fetchone(sql, self._category_id)

        if result is not None:
            return result[0]

    def set_name(self, name: str) -> None:
        """Set the categories name."""
        ActiveUser.get().raise_without_permission("menu.category.update.name")

        if not validate_menu_name(name):
            raise InputError("Inavlid category name")

        sql = "UPDATE public.menucategory SET name = %s WHERE id = %s"
        Database.execute(sql, name, self._category_id)

    def delete(self) -> None:
        """Delete the category, does not delete items."""
        ActiveUser.get().raise_without_permission("menu.category.delete")
        sql = "DELETE FROM public.menucategory WHERE id=%s;"
        Database.execute(sql, self._category_id)
