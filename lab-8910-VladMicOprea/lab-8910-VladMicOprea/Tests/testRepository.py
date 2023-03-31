from Domain.cardClient import CardClient
from Domain.medicament import Medicament
from Repository.repository import Repository


def testMedicamentReository():
    repo = Repository()
    repo.adauga(Medicament("1", "ibuprofen", "catena", 40.0, "da"))
    assert len(repo.read(Medicament)) == 1
    repo.modifica(Medicament("1", "ibuprofen", "bremen", 40.0, "da"))
    assert repo.read("1").producator == "bremen"
    repo.sterge("1")
    assert len(repo.read(Medicament)) == 0


def testCardClientRepository():
    repo = Repository()
    repo.adauga(CardClient("1", "Pop", "Andrei", "5070803303499", "13.02.2002", "23.03.2002"))
    assert len(repo.read(CardClient)) == 1
    repo.adauga(CardClient("2", "Pop", "Mihai", "5070803303522", "15.02.2002", "23.04.2002"))
    assert repo.read("2").nume == "Pop"


def testRepository():
    testMedicamentReository()
    testCardClientRepository()
