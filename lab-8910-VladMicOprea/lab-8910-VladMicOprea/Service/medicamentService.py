from Domain.addOperation import AddOperation
from Domain.deleteOperation import DeleteOperation
from Domain.medicament import Medicament
from Domain.medicamentValidator import MedicamentValidator
from Domain.modifyOperation import ModifyOperation
from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class MedicamentService:
    def __init__(self,
                 medicamentRepository: Repository,
                 medicamentValidator: MedicamentValidator,
                 undoRedoService: UndoRedoService):
        self.__medicamentRepository = medicamentRepository
        self.__medicamentValidator = medicamentValidator
        self.__undoRedoService = undoRedoService

    def getAll(self):
        return self.__medicamentRepository.read()

    def adauga(self, IdMedicament, nume, producator, pret, reteta):
        medicament = Medicament(IdMedicament, nume,
                                producator, pret, reteta)
        self.__medicamentValidator.valideaza(medicament)
        self.__medicamentRepository.adauga(medicament)
        self.__undoRedoService.addUndoOperation(
            AddOperation(self.__medicamentRepository, medicament))

    def sterge(self, IdMedicament):
        medicament = self.__medicamentRepository.read(IdMedicament)
        self.__medicamentRepository.sterge(IdMedicament)
        self.__undoRedoService.addUndoOperation(DeleteOperation(
            self.__medicamentRepository, medicament))

    def modifica(self, IdMedicament, nume, producator, pret, reteta):
        medicamentVechi = self.__medicamentRepository.read(IdMedicament)

        medicament = Medicament(IdMedicament, nume,
                                producator, pret, reteta)
        self.__medicamentValidator.valideaza(medicament)
        self.__medicamentRepository.modifica(medicament)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__medicamentRepository,
                            medicamentVechi, medicament))

    def cautare(self, text: str):
        lista = self.__medicamentRepository.read()
        return list(filter(lambda x: text in str(x.nume) or
                           text in str(x.producator) or
                           text in str(x.pret) or
                           text in str(x.reteta), lista))