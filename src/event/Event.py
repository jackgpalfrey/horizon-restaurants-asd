from ..utils.Database import Database
from src.user.ActiveUser import ActiveUser
from datetime import datetime
from src.user.Order import Order


class Event:
    def __init__(self, event_id: str):
        self._event_id = event_id

    def get_id(self) -> str | None:
        """Gets event ID"""
        event_id = Database.execute_and_fetchone(
            "SELECT event_id FROM public.events WHERE id = %d", self._event_id)
        assert event_id is not None

        return type[0]

    def get_event_type(self) -> str | None:
        """Gets event type"""
        type = Database.execute_and_fetchone(
            "SELECT type FROM public.events WHERE id = %d", self._event_id)
        assert type is not None

        return type[0]

    def get_phone_number(self) -> str | None:
        """Gets the phone number of whoever booked event"""
        phone_number = Database.execute_and_fetchone(
            "SELECT phone_number FROM public.events WHERE id = %s", self._event_id)
        assert phone_number is not None

        return phone_number[0]

    def get_email(self) -> str | None:
        """Gets the phone number of whoever booked event"""
        email = Database.execute_and_fetchone(
            "SELECT email FROM public.events WHERE id = %s", self._event_id)
        assert email is not None

        return email[0]

    def get_start_time(self) -> datetime | None:
        """Gets the time for the event"""
        start_time = Database.execute_and_fetchone(
            "SELECT start_time FROM public.events WHERE id = %s", self._event_id)
        assert start_time is not None

        return start_time[0]

    def get_end_time(self) -> datetime | None:
        """Gets the time for the event"""
        end_time = Database.execute_and_fetchone(
            "SELECT end_time FROM public.events WHERE id = %s", self._event_id)
        assert end_time is not None

        return end_time[0]

    def get_number(self) -> Order:
        """Get order's number."""
        sql = "SELECT number FROM public.order WHERE id=%s"
        result = Database.execute_and_fetchone(sql, self._order_id)
        assert result is not None
        return result[0]

    def set_type(self, type: str) -> None:
        """Set type of event"""
        ActiveUser.get().raise_without_permission("events.item.update.type")
        sql = "UPDATE public.events SET type = %s WHERE id = %s"
        Database.execute_and_commit(sql, type, self._event_id)

    def set_email(self, email: str) -> None:
        """Set user email for event"""
        ActiveUser.get().raise_without_permission("events.item.update.email")
        sql = "UPDATE public.events SET email = %s WHERE id = %s"
        Database.execute_and_commit(sql, email, self._event_id)

    def set_phone(self, phone: str) -> None:
        """Set user phone number for event"""
        ActiveUser.get().raise_without_permission("events.item.update.phone_number")
        sql = "UPDATE public.events SET phone_number = %s WHERE id = %s"
        Database.execute_and_commit(sql, phone, self._event_id)