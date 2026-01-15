from datetime import datetime
from typing import Optional
from src.db.models import TicketRequestModel, RequestStatus, TicketModel
from src.db.db_config import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class RefuseTicketRequestUseCase:

    def execute(self, request_id: str) -> Optional[TicketRequestModel]:
        with Session() as session:
            stmt = select(TicketRequestModel).options(
                joinedload(TicketRequestModel.ticket)
            ).where(TicketRequestModel.id == request_id)

            result = session.execute(stmt)
            request_model = result.scalar_one_or_none()

            if not request_model:
                return None

            if request_model.status != RequestStatus.PENDING:
                return None

            # Restituer le ticket réservé
            if request_model.ticket:
                ticket_model = request_model.ticket
                ticket_model.request_id = None
                ticket_model.available = True  # Le ticket redevient disponible

            request_model.status = RequestStatus.REFUSED
            session.commit()
            session.refresh(request_model)

            return request_model
