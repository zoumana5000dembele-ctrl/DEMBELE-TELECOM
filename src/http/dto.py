

from dataclasses import dataclass


@dataclass
class ListCategoryTicketDTO:
    id: str
    price: str
    name: str
    activity_time: str
    activity_time_unit: str
    stock_restant: int
