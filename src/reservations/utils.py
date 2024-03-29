# Author: Dina Hassanein (22066792)
"""Module with helpers and validation logic for reservations."""
from datetime import datetime
import re

from ..tables.Table import Table

CUSTOMER_NAME_MIN_LEN = 5  # INCLUSIVE
CUSTOMER_NAME_MAX_LEN = 50  # INCLUSIVE
CUSTOMER_NAME_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z ]*[a-zA-Z]$")


def validate_reservation_date(reservation_date: datetime):
    """Validate reservation date."""
    current_date = datetime.now()

    VALID_DATE = reservation_date >= current_date

    return VALID_DATE


def validate_customer_name(customer_name: str):
    """Validate customer name."""
    customer_name = customer_name.replace("  ", "!")

    ABOVE_MIN = len(customer_name) >= CUSTOMER_NAME_MIN_LEN
    BELOW_MAX = len(customer_name) <= CUSTOMER_NAME_MAX_LEN
    CORRECT_FORMAT = CUSTOMER_NAME_REGEX.match(customer_name) is not None

    return ABOVE_MIN and BELOW_MAX and CORRECT_FORMAT


def validate_guest_num(table: Table, guest_num: int):
    """Validate guest number."""
    table_capacity = table.get_capacity()
    CAPACITY_SUFFICIENT = table_capacity >= guest_num

    return CAPACITY_SUFFICIENT
