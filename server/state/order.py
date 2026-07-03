from dataclasses import dataclass, field


@dataclass
class OrderItem: # contains OrderMetadata
    item_name: str
    quantity: int

@dataclass
class OrderState:
    items: list[OrderItem] = field(default_factory=list)