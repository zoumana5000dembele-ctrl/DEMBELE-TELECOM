from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class CategoryTicket:
    id: UUID
    name: str
    activity_time: str
    created_at: datetime
