from Domain.cardClientValidator import CardClientValidator
from Domain.medicamentValidator import MedicamentValidator
from Repository.repositoryJson import RepositoryJson
from Service.cardClientService import CardClientService
from Service.medicamentService import MedicamentService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService
from UI.consola import Consola


def main():
    undoRedoService = UndoRedoService()

    medicamentRepositoryJson = RepositoryJson("medicament.json")
    medicamentValidator = MedicamentValidator()
    medicamentService = MedicamentService(medicamentRepositoryJson,
                                          medicamentValidator,
                                          undoRedoService)

    cardClientRepositoryJson = RepositoryJson("cardClient.json")
    cardClientValidator = CardClientValidator()
    cardClientService = CardClientService(cardClientRepositoryJson,
                                          cardClientValidator,
                                          undoRedoService)

    tranzactieRepositoryJson = RepositoryJson("tranzactie.json")
    tranzactieService = TranzactieService(tranzactieRepositoryJson,
                                          medicamentRepositoryJson,
                                          cardClientRepositoryJson,
                                          undoRedoService)

    consola = Consola(medicamentService,
                      cardClientService,
                      tranzactieService,
                      undoRedoService)

    consola.runMenu()


main()
