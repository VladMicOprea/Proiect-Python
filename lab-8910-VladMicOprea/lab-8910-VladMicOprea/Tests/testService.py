from Domain.cardClientValidator import CardClientValidator
from Domain.medicamentValidator import MedicamentValidator
from Repository.repository import Repository
from Service.cardClientService import CardClientService
from Service.medicamentService import MedicamentService


def testMedicamentService():
    medicamentRepository = Repository()
    medicamentValidator = MedicamentValidator()
    medicamentService = MedicamentService(medicamentRepository, medicamentValidator)
    medicamentService.adauga("1", "ibuprofen", "catena", 40.0, "da")
    assert len(medicamentService.getAll()) == 1


def testCardClientService():
    cardClientRepository = Repository()
    cardClientValidator = CardClientValidator()
    cardClientService = CardClientService(cardClientRepository, cardClientValidator)
    cardClientService.adauga("1", "Pop", "Andrei", "5070803303499", "13.02.2002", "23.03.2002")
    assert len(cardClientService.getAll()) == 1


def testService():
    testMedicamentService()
    testCardClientService()
