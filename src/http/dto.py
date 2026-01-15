

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ListCategoryTicketDTO:
    id: str
    price: str
    name: str
    activity_time: str
    activity_time_unit: str
    stock_restant: int


@dataclass
class TicketRequestDTO:
    id: str
    category_id: str
    category_name: str
    category_price: str
    client_name: str
    client_phone: str
    sms_content: Optional[str]
    status: str
    created_at: datetime
    validated_at: Optional[datetime]
    ticket_access_key: Optional[str] = None


@dataclass
class TicketRequestStatusDTO:
    id: str
    status: str
    category_name: str
    category_price: str
    created_at: datetime
    client_phone: Optional[str] = None
    ticket_access_key: Optional[str] = None
