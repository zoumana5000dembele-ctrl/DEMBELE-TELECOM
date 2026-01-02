from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship


TICKET_CATEGORY_TABLE_NAME: str = "category_ticket"


class CategoryTicketModel(SQLModel, table=True):
    __tablename__ = TICKET_CATEGORY_TABLE_NAME  # type: ignore

    id: UUID = Field(primary_key=True)
    name: str = Field(max_length=255)
    price: str = Field(default="0 FCFA", max_length=20)
    activity_time: str = Field(max_length=255)
    activity_time_unit: str = Field(max_length=20, default="H")
    created_at: datetime = Field(default_factory=datetime.now)

    # Relation
    tickets: List["TicketModel"] = Relationship(back_populates="category")


class TicketModel(SQLModel, table=True):
    __tablename__ = "ticket"  # type: ignore

    id: UUID = Field(primary_key=True)
    access_key: str = Field(max_length=255)
    active: bool = Field(default=True)
    category_id: UUID = Field(foreign_key=f"category_ticket.id")
    expires_in: datetime
    available: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relation
    category: Optional[CategoryTicketModel] = Relationship(
        back_populates="tickets")
