from Domain.entitate import Entitate
from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class DeleteOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, entitate: Entitate):
        self.__repository = repository
        self.__entitate = entitate

    def doUndo(self):
        self.__repository.adauga(self.__entitate)

    def doRedo(self):
        self.__repository.sterge(self.__entitate.IdEntitate)