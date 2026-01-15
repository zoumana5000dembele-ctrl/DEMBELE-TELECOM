from typing import Optional
from src.db.models import TicketRequestModel
from src.db.db_config import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class GetTicketRequestStatusUseCase:

    def execute(self, request_id: str) -> Optional[TicketRequestModel]:
        with Session() as session:
            stmt = select(TicketRequestModel).options(
                joinedload(TicketRequestModel.category),
                joinedload(TicketRequestModel.ticket),
            ).where(TicketRequestModel.id == request_id)

            result = session.execute(stmt)
            request_model = result.scalar_one_or_none()

            return request_model
