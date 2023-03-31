from Domain.cardClient import CardClient
from Domain.medicament import Medicament


def testMedicament():
    medicament = Medicament("1", "ibuprofen", "catena", 40.0, "da")

    assert medicament.reteta == "da"


def testCardClient():
    cardClient = CardClient("1", "Pop", "Andrei", "5070803303499", "13.02.2002", "23.03.2002")
    assert cardClient.nume == "Pop"


def testTranzactie():
    pass


def testDomain():
    testMedicament()
    testCardClient()
    testTranzactie()
