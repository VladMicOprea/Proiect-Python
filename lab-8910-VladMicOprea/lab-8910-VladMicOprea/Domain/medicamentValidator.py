from Domain.medicament import Medicament
from Domain.medicamentError import MedicamentError


class MedicamentValidator:
    def valideaza(self, medicament: Medicament):
        erori = []
        if medicament.pret <= 0:
            erori.append("Pretul trebuie sa fie strcit poztiv!")
        if len(erori) > 0:
            raise MedicamentError(erori)
