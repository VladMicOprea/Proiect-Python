from Domain.entitate import Entitate
from Repository.repository import Repository


class RepositoryInMemory(Repository):
    def __init__(self):
        self.entitati = {}

    def read(self, IdEntitate=None):
        if IdEntitate is None:
            return list(self.entitati.values())

        if IdEntitate in self.entitati:
            return self.entitati[IdEntitate]
        else:
            return None

    def adauga(self, entitate: Entitate):
        if self.read(entitate.IdEntitate) is not None:
            raise KeyError("Exista deja o entitate cu Id-ul dat!")
        self.entitati[entitate.IdEntitate] = entitate

    def sterge(self, IdEntitate: str):
        if self.read(IdEntitate) is None:
            raise KeyError("Nu exista nicio entitate cu Id-ul dat!")
        del self.entitati[IdEntitate]

    def modifica(self, entitate: Entitate):
        if self.read(entitate.IdEntitate) is None:
            raise KeyError("Nu exista nicio entitate cu Id-ul dat!")
        self.entitati[entitate.IdEntitate] = entitate
