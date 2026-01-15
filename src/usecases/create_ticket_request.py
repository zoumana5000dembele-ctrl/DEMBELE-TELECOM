from dataclasses import dataclass
from typing import Optional
from src.db.models import TicketRequestModel, RequestStatus, TicketModel
from src.db.db_config import Session
from src.entities.ticket_request import TicketRequest
from sqlalchemy import select


@dataclass
class CreateTicketRequestCommand:
    category_id: str
    client_name: str
    client_phone: str
    sms_content: Optional[str] = None


class CreateTicketRequestUseCase:

    def execute(self, command: CreateTicketRequestCommand) -> TicketRequest:
        request_entity = TicketRequest.create(
            category_id=command.category_id,
            client_name=command.client_name,
            client_phone=command.client_phone,
            sms_content=command.sms_content,
        )

        with Session() as session:
            # Réserver automatiquement un ticket disponible
            ticket_stmt = select(TicketModel).where(
                TicketModel.category_id == command.category_id,
                TicketModel.available == True,
                TicketModel.request_id.is_(None)
            ).limit(1)

            ticket_result = session.execute(ticket_stmt)
            ticket_model = ticket_result.scalar_one_or_none()

            if not ticket_model:
                raise ValueError("Aucun ticket disponible pour cette catégorie")

            request_model = TicketRequestModel(
                id=request_entity.id,
                category_id=request_entity.category_id,
                client_name=request_entity.client_name,
                client_phone=request_entity.client_phone,
                sms_content=request_entity.sms_content,
                status=RequestStatus.PENDING,
                created_at=request_entity.created_at,
            )

            # Réserver le ticket (ne pas le marquer comme non disponible, juste le lier)
            ticket_model.request_id = request_entity.id
            ticket_model.available = False  # Le ticket est réservé, donc non disponible

            session.add(request_model)
            session.commit()
            session.refresh(request_model)

        return request_entity
