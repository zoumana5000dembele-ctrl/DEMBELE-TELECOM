from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Ticket:
    id: UUID
    number: str
    access_key: str
    active: bool
    category_id: UUID
    expires_in: datetime
    available: bool
    created_at: datetime
