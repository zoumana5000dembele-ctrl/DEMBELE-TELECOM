from datetime import datetime
from uuid import UUID as _
from typing import List, Optional


from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
import enum

from src.db.db_config import Base
from src.entities.ticket import Ticket


TICKET_CATEGORY_TABLE_NAME: str = "category_ticket"


class RequestStatus(str, enum.Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    REFUSED = "refused"


class CategoryTicketModel(Base):
    __tablename__ = TICKET_CATEGORY_TABLE_NAME

    id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    price: Mapped[str] = mapped_column(
        String(20),
        default="0 FCFA",
        nullable=False,
    )

    activity_time: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    activity_time_unit: Mapped[str] = mapped_column(
        String(20),
        default="H",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )

    # Relations
    tickets: Mapped[List["TicketModel"]] = relationship(
        "TicketModel",
        back_populates="category",
        cascade="all, delete-orphan",
    )


class TicketModel(Base):
    __tablename__ = "ticket"

    id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
    )

    access_key: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    category_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("category_ticket.id"),
        nullable=False,
    )

    expires_in: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    available: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )

    # Relations
    category: Mapped[Optional[CategoryTicketModel]] = relationship(
        back_populates="tickets",
    )

    # Relation avec TicketRequest
    request_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        ForeignKey("ticket_request.id"),
        nullable=True,
    )

    request: Mapped[Optional["TicketRequestModel"]] = relationship(
        "TicketRequestModel",
        back_populates="ticket",
    )

    @staticmethod
    def from_entity(ticket: Ticket) -> "TicketModel":
        return TicketModel(
            id=ticket.id,
            access_key=ticket.access_key,
            category_id=ticket.category_id,
            active=ticket.active,
            expires_in=ticket.expires_in or datetime.now(),  # TODO à revoir
            available=ticket.available,
            created_at=ticket.created_at,
        )


class TicketRequestModel(Base):
    __tablename__ = "ticket_request"

    id: Mapped[str] = mapped_column(
        String(255),
        primary_key=True,
    )

    category_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("category_ticket.id"),
        nullable=False,
    )

    client_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    client_phone: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    sms_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(RequestStatus),
        default=RequestStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
    )

    validated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    # Relations
    category: Mapped[Optional[CategoryTicketModel]] = relationship(
        "CategoryTicketModel",
    )

    ticket: Mapped[Optional[TicketModel]] = relationship(
        "TicketModel",
        back_populates="request",
        uselist=False,
    )
