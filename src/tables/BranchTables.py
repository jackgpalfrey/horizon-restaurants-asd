# Author: Dina Hassanein (22066792)
"""Module for managing a branches tables."""
from src.utils.errors import AlreadyExistsError

from ..user.ActiveUser import ActiveUser
from ..utils.Database import Database
from .Table import Table
from .utils import validate_create_table


class BranchTables:
    """Class for managing a specific branches tables."""

    def __init__(self, branch_id: str):
        """Don't call outside of Branch."""
        self._branch_id = branch_id

    def create(self, table_number: int, table_capacity: int) -> Table:
        """
        Create a new table using the given parameters.

        A record of the created table is added to the database.
        :raises AuthorizationError: If active user does not have permission.
        """
        ActiveUser.get().raise_without_permission("table.create")

        if validate_create_table(table_number, self._branch_id) is True:
            raise AlreadyExistsError(
                "A table with this number already exists at this branch.")

        Database.execute_and_commit(
            "INSERT INTO public.table (table_number, capacity, branch_id) \
            VALUES(%s, %s, %s)", table_number, table_capacity, self._branch_id)
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.table \
            WHERE table_number = %s AND branch_id=%s;",
            table_number, self._branch_id)

        assert result is not None
        return Table(result[0])

    def get_by_id(self, table_id: str) -> Table | None:
        """
        Get a table by its ID.

        Note: This is not limited to this branch.
        """
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.table WHERE id = %s AND branch_id = %s;",
            table_id, self._branch_id)

        if result is not None:
            return Table(result[0])

    def get_by_number(self, table_number: int) -> Table | None:
        """Get a table by it's number."""
        result = Database.execute_and_fetchone(
            "SELECT id FROM public.table WHERE table_number = %s \
            AND branch_id = %s;", table_number, self._branch_id)

        if result is not None:
            return Table(result[0])

    def find_by_capacity(self, table_capacity: int) -> list[Table]:
        """
        Get tables that have a capacity equal or higher than the given size.

        :returns list of tables in ascending order of capacity. i.e the lowest
        capacity above or equal to the minimum will be first.
        """
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.table WHERE capacity >= %s \
            AND branch_id = %s ORDER BY capacity",
            table_capacity, self._branch_id)

        return [Table(record[0]) for record in result]

    def get_all(self) -> list[Table]:
        """Get all tables at the branch."""
        result = Database.execute_and_fetchall(
            "SELECT id FROM public.table WHERE branch_id = %s;",
            self._branch_id)

        return [Table(record[0]) for record in result]
