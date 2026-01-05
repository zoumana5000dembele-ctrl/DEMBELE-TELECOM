
from dataclasses import dataclass
from src.db.models import TicketModel
from src.db.db_config import session
from typing import List

from src.entities.ticket import Ticket


@dataclass
class AddTicketsCommand:
    access_keys: List[str]
    category_id: str


class AddTicketsUseCase:

    def execute(self, _tickets: AddTicketsCommand) -> List[Ticket]:
        # Construire le ticket à partir de la commande
        tickets: List[Ticket] = [Ticket.create_from_access_key(
            access_key, _tickets.category_id) for access_key in _tickets.access_keys]

        # Persister les tickets dans la base de données

        tickets_models = [
            TicketModel.from_entity(ticket) for ticket in tickets
        ]

        session.add_all(tickets_models)
        session.commit()

        return tickets
