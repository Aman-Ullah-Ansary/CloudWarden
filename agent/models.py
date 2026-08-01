from dataclasses import dataclass


@dataclass
class NamespaceCost:

    namespace: str

    total_cost: float
    