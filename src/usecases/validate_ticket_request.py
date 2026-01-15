from datetime import datetime
from typing import Optional
from src.db.models import (
    TicketRequestModel,
    RequestStatus,
)
from src.db.db_config import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class ValidateTicketRequestUseCase:

    def execute(self, request_id: str) -> Optional[TicketRequestModel]:
        with Session() as session:
            # Récupérer la demande avec son ticket réservé
            stmt = select(TicketRequestModel).options(
                joinedload(TicketRequestModel.category),
                joinedload(TicketRequestModel.ticket)
            ).where(TicketRequestModel.id == request_id)

            result = session.execute(stmt)
            request_model = result.scalar_one_or_none()

            if not request_model:
                return None

            if request_model.status != RequestStatus.PENDING:
                return None

            # Le ticket est déjà réservé, on valide juste la demande
            # Le ticket reste lié à la demande (request_id déjà défini)
            request_model.status = RequestStatus.VALIDATED
            request_model.validated_at = datetime.now()

            session.commit()
            session.refresh(request_model)

            return request_model
