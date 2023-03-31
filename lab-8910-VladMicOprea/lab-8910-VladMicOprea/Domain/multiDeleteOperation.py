from Domain.undoRedoOperation import UndoRedoOperation
from Repository.repository import Repository


class MultiDeleteOperation(UndoRedoOperation):
    def __init__(self, repository: Repository, obiecteSterse):
        self.repository = repository
        self.obiecteSterse = obiecteSterse

    def do_undo(self):
        for entitate in self.obiecteSterse:
            self.repository.adauga(entitate)

    def do_redo(self):
        for entitate in self.obiecteSterse:
            self.repository.sterge(entitate.id_entitate)
