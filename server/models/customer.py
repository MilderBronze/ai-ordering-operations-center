import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class PaymentMode(enum.Enum):
    CREDIT_CARD = "credit_card"
    UPI = "upi"
    CASH = "cash"


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    payment_mode: Mapped[PaymentMode] = mapped_column(
        Enum(PaymentMode),
        nullable=False,
    )
