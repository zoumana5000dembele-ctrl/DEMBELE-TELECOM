
from typing import List
from sqlmodel import select
from sqlalchemy.orm import joinedload
from src.db.db_config import session
from src.db.models import CategoryTicketModel
from src.http.dto import ListCategoryTicketDTO


class ListTicketsCategoriesUseCase:

    def execute(self) -> List[ListCategoryTicketDTO]:
        stmt = select(CategoryTicketModel).options(
            joinedload(CategoryTicketModel.tickets))  # type: ignore
        category_models = session.exec(stmt).unique().all()

        categories = [
            ListCategoryTicketDTO(
                id=str(category.id),
                price=str(category.price),
                name=category.name,
                activity_time_unit=category.activity_time_unit,
                activity_time=category.activity_time,
                stock_restant=len(category.tickets)
            )
            for category in category_models
        ]

        return categories
