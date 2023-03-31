from dataclasses import dataclass

from Domain.medicament import Medicament


@dataclass
class MedicamentViewModel:
    medicament = Medicament
    nrBucata = int

    def __init__(self, medicament, nrBucata):
        self.medicament = medicament
        self.nrBucata = nrBucata

    def __str__(self):
        return f'{self.medicament} are vanzarea {self.nrBucata}'
