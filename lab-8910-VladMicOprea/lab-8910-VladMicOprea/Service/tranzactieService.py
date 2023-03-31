from functools import reduce

from Domain.addOperation import AddOperation
from Domain.cascadaDelete import CascadeDelete
from Domain.deleteOperation import DeleteOperation
from Domain.modifyOperation import ModifyOperation
from Domain.multiDeleteOperation import MultiDeleteOperation
from Domain.tranzactie import Tranzactie

from Repository.repository import Repository
from Service.undoRedoService import UndoRedoService


class TranzactieService:
    def __init__(self,
                 tranzactieRepository: Repository,
                 medicamentRepository: Repository,
                 cardClientRepository: Repository,
                 undoRedoService: UndoRedoService):
        self.__medicamentRepository = medicamentRepository
        self.__tranzactieRepository = tranzactieRepository
        self.__cardClientRepository = cardClientRepository
        self.__undoRedoService = undoRedoService

    def getAll(self):
        return self.__tranzactieRepository.read()

    def adauga(self, IdTranzactie, IdMedicament,
               IdCardClient, nrBucati, data, ora):
        if self.__medicamentRepository.read(IdMedicament) is None:
            raise KeyError("Nu exista niciun medicament cu id-ul dat!")
        if self.__cardClientRepository.read(IdCardClient) is None:
            raise KeyError("Nu exista niciun card client cu id-ul dat!")

        if self.__cardClientRepository is not None:
            medicament = self.__medicamentRepository.read(IdMedicament)
            if medicament.reteta == "Nu":
                medicament.pret = medicament.pret - medicament.pret * 0.1
                print(medicament.pret, "10%")
            elif medicament.reteta == "Da":
                medicament.pret = medicament.pret - medicament.pret * 0.15
                print(medicament.pret, "15%")

        tranzactie = Tranzactie(IdTranzactie, IdMedicament,
                                IdCardClient, nrBucati, data, ora)

        self.__tranzactieRepository.adauga(tranzactie)
        self.__undoRedoService.addUndoOperation(AddOperation(
            self.__tranzactieRepository, tranzactie))

    def sterge(self, IdTranzactie):
        tranzactie = self.__tranzactieRepository.read(IdTranzactie)
        self.__tranzactieRepository.sterge(IdTranzactie)
        self.__undoRedoService.addUndoOperation(DeleteOperation(
            self.__tranzactieRepository, tranzactie))

    def modifica(self, IdTranzactie, IdMedicament,
                 IdCardClient, nrBucati, data, ora):
        if self.__medicamentRepository.read(IdMedicament) is None:
            raise KeyError("Nu exista niciun medicament cu id-ul dat!")
        if self.__cardClientRepository.read(IdCardClient) is None:
            raise KeyError("Nu exista niciun card client cu id-ul dat!")

        tranzactieVeche = self.__tranzactieRepository.read(IdTranzactie)
        tranzactie = Tranzactie(IdTranzactie, IdMedicament,
                                IdCardClient, nrBucati, data, ora)

        self.__tranzactieRepository.modifica(tranzactie)
        self.__undoRedoService.addUndoOperation(
            ModifyOperation(self.__tranzactieRepository,
                            tranzactieVeche, tranzactie))

    def cautare(self, text):
        rezultat = []
        for medicament in self.__medicamentRepository.read():
            if text in str(medicament.IdEntitate) or \
                    text in str(medicament.nume) or \
                    text in str(medicament.producator) or \
                    text in str(medicament.pret) or \
                    text in str(medicament.reteta):
                rezultat.append(medicament)
        for cardClient in self.__cardClientRepository.read():
            if text in str(cardClient.IdEntitate) or \
                    text in str(cardClient.nume) or \
                    text in str(cardClient.prenume) or \
                    text in str(cardClient.CNP) or \
                    text in str(cardClient.dataNasterii) or \
                    text in str(cardClient.dataInregistrarii):
                rezultat.append(cardClient)
        return rezultat

    def intervalTranzactii(self, prima_data, ultima_data, lista_tranzactii,
                           rezultat):
        if len(lista_tranzactii) == 0:
            if not rezultat:
                raise KeyError(f'Nu exista tranzactii intre '
                               f'{prima_data} si {ultima_data}!')
            return rezultat
        if prima_data < lista_tranzactii[-1].data_si_ora.date() < ultima_data:
            rezultat.append(lista_tranzactii[-1])
        return self.intervalTranzactii(prima_data, ultima_data,
                                       lista_tranzactii[:-1], rezultat)

    def my_sorted(self, lista, key=None, reverse=False):
        if reverse is False:
            for i in range(len(lista) - 1):
                for j in range(i + 1, len(lista)):
                    if key(lista[i]) > key(lista[j]):
                        lista[i], lista[j] = lista[j], lista[i]
        else:
            for i in range(len(lista) - 1):
                for j in range(i + 1, len(lista)):
                    if key(lista[i]) < key(lista[j]):
                        lista[i], lista[j] = lista[j], lista[i]
        return lista

    def medicamenteOrdonateDescrescatorDupaVanzari(self):
        vanzariPerMedicamente = {}
        rezultat = []
        for medicament in self.__medicamentRepository.read():
            vanzariPerMedicamente[medicament.IdEntitate] = []
        for tranzactie in self.__tranzactieRepository.read():
            vanzariPerMedicamente[tranzactie.IdMedicament].append(
                tranzactie.nrBucati)
        for IdMedicament in vanzariPerMedicamente:
            vanzari = vanzariPerMedicamente[IdMedicament]
            rezultat.append({
                "medicament": self.__medicamentRepository.read(IdMedicament),
                "nrVanzari": reduce(lambda x, y: x + y, vanzari)
            })

        return self.my_sorted(rezultat,
                              key=lambda nrV: nrV["nrVanzari"], reverse=True)

    def carduriClientOrdonateDescrescatorDupaValoareaReducerilor(self):
        valoriReduceri = {}
        rezultat = []
        for cardClient in self.__cardClientRepository.read():
            valoriReduceri[cardClient.IdEntitate] = []
        for tranzactie in self.__tranzactieRepository.read():
            if self.__medicamentRepository.read(tranzactie.IdMedicament).reteta == "Da":
                pret = self.__medicamentRepository.read(
                    tranzactie.IdMedicament).pret * int(tranzactie.nrBucati) * 15 // 100
                valoriReduceri[tranzactie.IdCardClient].append(pret)
            else:
                pret = self.__medicamentRepository.read(
                    tranzactie.IdMedicament).pret * int(tranzactie.nrBucati) * 10 // 100
                valoriReduceri[tranzactie.IdCardClient].append(pret)

        for IdCardClient in valoriReduceri:
            reduceri = valoriReduceri[IdCardClient]

            if len(reduceri) == 1:
                rezultat.append({
                    "cardClient": self.__cardClientRepository.read(IdCardClient),
                    "valoareReducere": reduceri[0]
                })
            elif len(reduceri) > 1:
                rezultat.append({
                    "cardClient": self.__cardClientRepository.read(IdCardClient),
                    "valoareReducere": reduce(lambda x, y: x + y, reduceri)
                })
        return self.my_sorted(rezultat,
                              key=lambda tranzactiePerCardClient: tranzactiePerCardClient["valoareReducere"],
                              reverse=True)

    def stergereTranzactiiIntervalDeZileDat(self, primaZi, ultimaZi):
        exista = False
        listaTranzactii = self.__tranzactieRepository.read()
        tranzactiiSterse = []

        tranzactiiDeSters = [tranzactie for tranzactie in listaTranzactii if
                             primaZi <= tranzactie.data
                             <= ultimaZi]

        for tranz in tranzactiiDeSters:
            tranzactiiSterse.append(tranz)
            self.sterge(tranz.IdEntitate)
        self.__undoRedoService.addUndoOperation(
             MultiDeleteOperation(self.__tranzactieRepository,
                                  tranzactiiSterse))
        if len(tranzactiiDeSters) > 0:
            exista = True
        if exista is False:
            raise KeyError(
                f'Nu exista nicio tranzactie intre {primaZi} si {ultimaZi}!')

        return tranzactiiSterse

    def scumpireMedicamente(self, procent, valoare):
        for medicament in self.__medicamentRepository.read():
            if medicament.pret < valoare:
                medicament.pret = medicament.pret + medicament.pret * procent // 100
                self.__medicamentRepository.modifica(medicament)

    def stergereInCascadaMedicament(self, IdMedicament):
        medicamenteSterse = []
        tranzactiiSterse = []
        for medicament in self.__medicamentRepository.read():
            if medicament.IdEntitate == IdMedicament:
                medicamenteSterse.append(medicament)
                self.__medicamentRepository.sterge(medicament.IdEntitate)
                for tranzactie in self.__tranzactieRepository.read():
                    if tranzactie.IdMedicament == IdMedicament:
                        tranzactiiSterse.append(tranzactie)
                        self.__tranzactieRepository.sterge(tranzactie.IdEntitate)

        self.__undoRedoService.addUndoOperation(
            CascadeDelete(self.__medicamentRepository, self.__tranzactieRepository,
                          medicamenteSterse, tranzactiiSterse)
        )

    def stergereInCascadaCardClient(self, IdCardClient):
        carduriClientSterse = []
        tranzactiiSterse = []
        for cardClient in self.__cardClientRepository.read():
            if cardClient.IdEntitate == IdCardClient:
                carduriClientSterse.append(cardClient)
                self.__cardClientRepository.sterge(cardClient.IdEntitate)
                for tranzactie in self.__tranzactieRepository.read():
                    if tranzactie.IdCardClient == IdCardClient:
                        tranzactiiSterse.append(tranzactie)
                        self.__tranzactieRepository.sterge(tranzactie.IdEntitate)
        self.__undoRedoService.addUndoOperation(
            CascadeDelete(self.__cardClientRepository, self.__tranzactieRepository,
                          carduriClientSterse, tranzactiiSterse)
        )
