from Domain.addOperation import AddOperation
from Domain.cardClient import CardClient
from Domain.cardClientValidator import CardClientValidator
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class CardClientService:
    def __init__(self,
                 cardClientRepository: Repository,
                 cardClientValidator: CardClientValidator,
                 undoRedoService: UndoRedoService):
        self.__cardClientRepository = cardClientRepository
        self.__cardClientValidator = cardClientValidator
        self.__undoRedoService = undoRedoService

    def getAll(self):
        return self.__cardClientRepository.read()

    def adauga(self, IdCardClient, nume, prenume,
               CNP, dataNasterii, dataInregistrarii):
        cardClient = CardClient(IdCardClient, nume,
                                prenume, CNP, dataNasterii,
                                dataInregistrarii)
        self.__cardClientValidator.valideaza(cardClient)
        self.__cardClientRepository.adauga(cardClient)
        self.__undoRedoService.addUndoOperation(
            AddOperation(self.__cardClientRepository, cardClient)
        )

    def sterge(self, IdCardClient):
        cardClient = self.__cardClientRepository.read(IdCardClient)
        self.__cardClientRepository.sterge(IdCardClient)
        self.__undoRedoService.addUndoOperation(
            DeleteOperation(self.__cardClientRepository, cardClient))

    def modifica(self, IdCardClient, nume, prenume,
                 CNP, dataNasterii, dataInregistrarii):
        cardClientVechi = self.__cardClientRepository.read(IdCardClient)
        cardClient = CardClient(IdCardClient, nume, prenume,
                                CNP, dataNasterii, dataInregistrarii)
        self.__cardClientValidator.valideaza(cardClient)
        self.__cardClientRepository.modifica(cardClient)
        self.__undoRedoService.addUndoOperation(ModifyOperation(
            self.__cardClientRepository,
            cardClientVechi,
            cardClient))

    def cautare(self, text: str):
        lista = self.__cardClientRepository.read()
        return list(filter(lambda x: text in str(x.nume) or
                           text in str(x.prenume) or
                           text in str(x.CNP) or
                           text in str(x.dataNasterii) or
                           text in str(x.dataInregistrarii), lista))