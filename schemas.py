from pydantic import BaseModel, validator
from datetime import datetime
from typing import Literal

class SearchQuery(BaseModel):
    origin_city: str
    destination_city: str
    departure_date: datetime
    adults: int
    children: int
    infants: int
    extra: int  # если 4-я цифра что-то значит — можешь позже уточнить
    travel_class: Literal["E", "B", "F"]

    @classmethod
    def from_search_string(cls, query: str) -> "SearchQuery":
        try:
            # Пример: AKX-ALA202401022000E
            route = query[:7]              # AKX-ALA
            date_str = query[7:15]         # 20240102
            pax_str = query[15:19]         # 2000
            class_code = query[19]         # E

            origin, destination = route.split('-')
            departure_date = datetime.strptime(date_str, "%Y%m%d")

            return cls(
                origin_city=origin,
                destination_city=destination,
                departure_date=departure_date,
                adults=int(pax_str[0]),
                children=int(pax_str[1]),
                infants=int(pax_str[2]),
                extra=int(pax_str[3]),
                travel_class=class_code
            )
        except Exception as e:
            raise ValueError(f"Invalid search query format: {e}")
