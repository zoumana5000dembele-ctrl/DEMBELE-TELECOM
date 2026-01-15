
from dataclasses import dataclass
from typing import List

from src.db.models import TicketModel
from src.db.db_config import Session
from src.entities.ticket import Ticket


@dataclass
class AddTicketsCommand:
    access_keys: List[str]
    category_id: str


class AddTicketsUseCase:

    def execute(self, _tickets: AddTicketsCommand) -> List[Ticket]:
        # Construire les entités Ticket à partir de la commande
        tickets: List[Ticket] = [
            Ticket.create_from_access_key(access_key, _tickets.category_id)
            for access_key in _tickets.access_keys
        ]

        # Persister les tickets via SQLAlchemy
        tickets_models = [TicketModel.from_entity(ticket) for ticket in tickets]

        with Session() as session:
            session.add_all(tickets_models)
            session.commit()

        return tickets
