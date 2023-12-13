from ..utils.Database import Database
from ..city.City import City


class CityService:
    @staticmethod
    def create(city_name: str) -> City:
        Database.execute_and_commit(
            "INSERT INTO public.city (name) VALUES(%s)", city_name)
        city_id = Database.execute_and_fetchone(
            "SELECT id FROM public.city WHERE name = %s", city_name)
        return City(city_id)
