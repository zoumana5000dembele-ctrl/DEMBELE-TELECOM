from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Ticket:
    id: str
    number: str
    access_key: str
    category_id: str
    active: bool = True
    expires_in: Optional[datetime] = None
    available: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def create_from_access_key(access_key: str, category_id: str) -> 'Ticket':
        return Ticket(
            id=str(uuid4()),
            number=str(uuid4()),
            access_key=access_key,
            category_id=category_id
        )
