from dataclasses import dataclass, field

@dataclass
class OrderState:
    items: list[dict] = field(default_factory=list)