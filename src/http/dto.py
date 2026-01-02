

from dataclasses import dataclass


@dataclass
class ListCategoryTicketDTO:
    id: str
    price: str
    activity_time: str
    activity_time_unit: str
