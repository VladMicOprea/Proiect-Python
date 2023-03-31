from dataclasses import dataclass

from Domain.entitate import Entitate


@dataclass
class Tranzactie(Entitate):
    IdMedicament: str
    IdCardClient: str
    nrBucati: int
    data: str
    ora: str
