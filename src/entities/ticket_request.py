from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class TicketRequest:
    id: str
    category_id: str
    client_name: str
    client_phone: str
    sms_content: Optional[str] = None
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    validated_at: Optional[datetime] = None

    @staticmethod
    def create(
        category_id: str,
        client_name: str,
        client_phone: str,
        sms_content: Optional[str] = None,
    ) -> 'TicketRequest':
        return TicketRequest(
            id=str(uuid4()),
            category_id=category_id,
            client_name=client_name,
            client_phone=client_phone,
            sms_content=sms_content,
            status="pending",
        )
