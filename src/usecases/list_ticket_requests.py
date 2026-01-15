from typing import List, Optional
from src.db.models import TicketRequestModel, RequestStatus
from src.db.db_config import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class ListTicketRequestsUseCase:

    def execute(self, status: Optional[RequestStatus] = None) -> List[TicketRequestModel]:
        with Session() as session:
            stmt = select(TicketRequestModel).options(
                joinedload(TicketRequestModel.category),
                joinedload(TicketRequestModel.ticket),
            )

            if status:
                stmt = stmt.where(TicketRequestModel.status == status)
            else:
                # Par défaut, retourner seulement les demandes en attente
                stmt = stmt.where(TicketRequestModel.status == RequestStatus.PENDING)

            stmt = stmt.order_by(TicketRequestModel.created_at.desc())

            result = session.execute(stmt)
            requests = result.scalars().unique().all()

            return list(requests)
