
from typing import List
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from src.db.db_config import Session
from src.db.models import CategoryTicketModel, TicketModel
from src.http.dto import ListCategoryTicketDTO


class ListTicketsCategoriesUseCase:

    def execute(self) -> List[ListCategoryTicketDTO]:
        with Session() as session:
            stmt = select(CategoryTicketModel).options(
                joinedload(CategoryTicketModel.tickets))

            result = session.execute(stmt)
            category_models = result.scalars().unique().all()

            categories : List[ListCategoryTicketDTO] = []
            for category in category_models:
                # Compter uniquement les tickets disponibles (available=True et request_id=None)
                count_stmt = select(func.count(TicketModel.id)).where(
                    TicketModel.category_id == category.id,
                    TicketModel.available == True,
                    TicketModel.request_id.is_(None)
                )
                stock_count = session.execute(count_stmt).scalar() or 0

                categories.append(
                    ListCategoryTicketDTO(
                        id=str(category.id),
                        price=str(category.price),
                        name=category.name,
                        activity_time_unit=category.activity_time_unit,
                        activity_time=category.activity_time,
                        stock_restant=stock_count
                    )
                )

            return categories
