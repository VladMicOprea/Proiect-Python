from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultiUpdateOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiecteNoiModificate, obiecteVechiModificate):
        self.repository = repository
        self.obiecteNoiModificate = obiecteNoiModificate
        self.obiecteVechiModificate = obiecteVechiModificate

    def do_undo(self):
        for entitate in self.obiecteVechiModificate:
            self.repository.modifica(entitate)

    def do_redo(self):
        for entitate in self.obiecteNoiModificate:
            self.repository.modifica(entitate)
