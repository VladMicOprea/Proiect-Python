from abc import ABC
from dataclasses import dataclass


@dataclass
class Entitate(ABC):
    IdEntitate: str
