import enum
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class OrderType(enum.Enum):
    TAKEAWAY = "takeaway"
    DELIVERY = "delivery"
    DINE_IN = "dine_in"


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.customer_id"),
        nullable=False,
    )

    order_type: Mapped[OrderType] = mapped_column(
        Enum(OrderType),
        nullable=False,
    )

    total_bill_amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )