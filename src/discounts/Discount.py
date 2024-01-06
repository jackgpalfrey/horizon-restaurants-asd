from src.utils.errors import InputError
from ..utils.Database import Database
from .utils import validate_description

class Discounts:
    _discount_id: str

    def __init__(self, discount_id: str) -> None:
        self._discount_id = discount_id

    def get_description(self) -> str:
        """Get description."""
        description = Database.execute_and_fetchone(
                "SELECT description FROM public.discounts WHERE id= %s", self._discount_id)
        assert description is not None

        return description[0]
    
    def get_multiplier(self) -> float:
        """Get description."""
        multiplier = Database.execute_and_fetchone(
                "SELECT multiplier FROM public.discounts WHERE id= %s", self._discount_id)
        assert multiplier is not None

        return multiplier[0]
    
    def set_description(self, description: str) -> None:
        if not validate_description(description):
            raise InputError("Invalid description.")
        
        Database.execute_and_commit(
            "UPDATE public.discounts SET description = %s WHERE id = %s",description, self._discount_id)

    def set_multiplier(self, multiplier: float) -> None:
        
        Database.execute_and_commit(
            "UPDATE public.discounts SET multiplier = %s WHERE id = %s",multiplier, self._discount_id)