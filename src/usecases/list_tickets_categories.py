
from typing import List
from sqlmodel import select
from src.db.db_config import session
from src.db.models import CategoryTicketModel
from src.http.dto import ListCategoryTicketDTO


class ListTicketsCategoriesUseCase:

    def execute(self) -> List[ListCategoryTicketDTO]:
        stmt = select(CategoryTicketModel)
        categories = session.exec(stmt).all()

        categories = [
            ListCategoryTicketDTO(
                id=str(category.id),
                price=str(category.price),
                activity_time_unit=category.activity_time_unit,
                activity_time=category.activity_time
            )
            for category in categories
        ]

        return categories
