import datetime
import random

from Domain.medicamentError import MedicamentError
from Service.cardClientService import CardClientService
from Service.medicamentService import MedicamentService
from Service.tranzactieService import TranzactieService
from Service.undoRedoService import UndoRedoService


class Consola:
    def __init__(self,
                 medicamentService: MedicamentService,
                 cardClientService: CardClientService,
                 tranzactieService: TranzactieService,
                 undoRedoService: UndoRedoService):
        self.__cardClientService = cardClientService
        self.__medicamentService = medicamentService
        self.__tranzactieService = tranzactieService
        self.__undoRedoService = undoRedoService

    def runMenu(self):
        while True:
            print("1. CRUD medicament")
            print("2. CRUD card client")
            print("3. CRUD tranzactie")
            print("4. Cautare full text")
            print("5. Afisare tranzactii intr-un interval de zile dat")
            print("6. Afișarea medicamentelor ordonate "
                  "descrescător după numărul de vânzări")
            print("7. Afișarea cardurilor client ordonate descrescător după valoarea reducerilor obținute")
            print("8. Stergere tranzactii intr-un interval de zile dat")
            print("9. Scumpirea cu un procentaj dat a "
                  "tuturor medicamentelor cu prețul "
                  "mai mic decât o valoare dată")
            print("ran. Random")
            print("s. Stergere in cascada")
            print("u. Undo")
            print("r. Redo")
            print("x. Iesire")
            optiune = input("Dati optiunea: ")

            if optiune == "1":
                self.runCRUDMedicamentMenu()
            elif optiune == "2":
                self.runCRUDCardClient()
            elif optiune == "3":
                self.runCRUDTranzactie()
            elif optiune == "4":
                self.uiCautare()
            elif optiune == "5":
                self.uiTranzactiiIntervalDeZileDat()
            elif optiune == "6":
                self.uiMedicamenteOrdonateDescrescatorDupaVanzari()
            elif optiune == "7":
                self.uiCarduriClientOrdonateDescrescatorDupaValoareaReducerilor()
            elif optiune == "8":
                self.uiStergereTranzactiiIntervalDeZileDat()
            elif optiune == "9":
                self.uiScumpireMedicament()
            elif optiune == "ran":
                self.uiRandom()
            elif optiune == "s":
                self.uiStergereInCascada()
            elif optiune == "u":
                self.__undoRedoService.undo()
            elif optiune == "r":
                self.__undoRedoService.redo()
            elif optiune == "x":
                break
            else:
                print("Optiune gresita! Reincercati: ")

    def uiAdaugaMedicament(self):
        try:
            IdMedicament = input("Dati Id-ul medicamentului: ")
            nume = input("Dati numele medicamentului: ")
            producator = input("Dati producatorul medicamentului: ")
            pret = int(input("Dati pretul medicamentului: "))
            reteta = input("Dati necesita reteta medicamentului: ")

            self.__medicamentService.adauga(IdMedicament, nume,
                                            producator, pret, reteta)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeMedicament(self):
        try:
            IdMedicament = input("Dati Id-ul medicamentului: ")

            self.__medicamentService.sterge(IdMedicament)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaMedicament(self):
        try:
            IdMedicament = input("Dati Id-ul medicamentului: ")
            nume = input("Dati numele medicamentului: ")
            producator = input("Dati producatorul medicamentului: ")
            pret = int(input("Dati pretul medicamentului: "))
            reteta = input("Dati necesita reteta medicamentului: ")

            self.__medicamentService.modifica(IdMedicament, nume,
                                              producator, pret, reteta)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiCautareMedicament(self):
        try:
            text = input("Introduceti textul: ")
            for rezultat in self.__medicamentService.cautare(text):
                print(rezultat)
        except ValueError as ve:
            print(ve)

    def showAllMedicamente(self):
        for medicament in self.__medicamentService.getAll():
            print(medicament)

    def runCRUDCardClient(self):
        print("1. Adauga card client")
        print("2. Sterge card client")
        print("3. Modifica card client")
        print("4. Cautare card client")
        print("a. Afiseaza toate cardurile client")
        print("x. Iesire")
        optiune = input("Dati optiunea: ")

        if optiune == "1":
            self.uiAdaugaCardClient()
        elif optiune == "2":
            self.uiStergeCardClient()
        elif optiune == "3":
            self.uiModificaCardClient()
        elif optiune == "4":
            self.uiCautareCardClient()
        elif optiune == "a":
            self.showAllCardClient()
        else:
            print("Optiune gresita! Reincercati: ")

    def uiAdaugaCardClient(self):
        try:
            IdCardClient = input("Dati Id-ul cardului client: ")
            nume = input("Dati numele cardului client: ")
            prenume = input("Dati  prenumele cardului client: ")
            CNP = input("Dati CNP-ul cardului client: ")
            dataNasterii = input("Dati data nasterii cardului client: ")
            dataInregistrarii = input("Dati data inregistarii cardului client: ")

            dataNasterii = datetime.datetime.strptime(
                dataNasterii, '%d-%m-%Y').date()
            dataInregistrarii = datetime.datetime.strptime(
                dataInregistrarii, '%d-%m-%Y').date()

            self.__cardClientService.adauga(IdCardClient, nume,
                                            prenume, CNP, dataNasterii,
                                            dataInregistrarii)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeCardClient(self):
        try:
            IdCardClient = input("Dati Id-ul cardului client: ")

            self.__cardClientService.sterge(IdCardClient)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaCardClient(self):
        try:
            IdCardClient = input("Dati Id-ul cardului client: ")
            nume = input("Dati numele cardului client: ")
            prenume = input("Dati  prenumele cardului client: ")
            CNP = input("Dati CNP-ul cardului client: ")
            dataNasterii = input("Dati data nasterii cardului client: ")
            dataInregistrarii = input("Dati data inregistarii cardului client: ")

            dataNasterii = datetime.datetime.strptime(
                dataNasterii, '%d-%m-%Y').date()
            dataInregistrarii = datetime.datetime.strptime(
                dataInregistrarii, '%d-%m-%Y').date()

            self.__cardClientService.modifica(IdCardClient, nume,
                                              prenume, CNP, dataNasterii,
                                              dataInregistrarii)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiCautareCardClient(self):
        try:
            text = input("Introduceti textul: ")
            for rezultat in self.__cardClientService.cautare(text):
                print(rezultat)
        except ValueError as ve:
            print(ve)

    def showAllCardClient(self):
        for cardClient in self.__cardClientService.getAll():
            print(cardClient)

    def runCRUDTranzactie(self):
        print("1. Adauga tranzactie")
        print("2. Sterge tranzactie")
        print("3. Modifica tranzactie")
        print("a. Afiseaza toate tranzactiile")
        print("x. Iesire")
        optiune = input("Dati optiunea: ")

        if optiune == "1":
            self.uiAdaugaTranzactie()
        elif optiune == "2":
            self.uiStergeTranzactie()
        elif optiune == "3":
            self.uiModificaTranzactie()
        elif optiune == "a":
            self.showAllTranzactie()
        else:
            print("Optiune gresita! Reincercati: ")

    def uiAdaugaTranzactie(self):
        try:
            IdTranzactie = input("Dati Id-ul tranzactiei: ")
            IdMedicament = input("Dati Id-ul medicamentului: ")
            IdCardClient = input("Dati Id-ul cardului client: ")
            nrBucati = input("Dati numarul de bucati al tranzactiei: ")
            data = input("Dati data tranzactiei: ")
            ora = input("Dati ora tranzactiei")

            data = datetime.datetime.strptime(data, '%d-%m-%Y').date()
            ora = datetime.datetime.strptime(ora, '%H:%M').date()

            self.__tranzactieService.adauga(IdTranzactie, IdMedicament,
                                            IdCardClient, nrBucati,
                                            data, ora)
        except ValueError as ve:
            print(ve)
        except MedicamentError as me:
            print(me)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiStergeTranzactie(self):
        try:
            IdTranzactie = input("Dati Id-ul tranzactiei de sters: ")

            self.__tranzactieService.sterge(IdTranzactie)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def uiModificaTranzactie(self):
        try:
            IdTranzactie = input("Dati Id-ul tranzactiei: ")
            IdMedicament = input("Dati Id-ul medicamentului: ")
            IdCardClient = input("Dati Id-ul cardului client: ")
            nrBucati = int(input("Dati numarul de bucati al tranzactiei: "))
            data = input("Dati data tranzactiei: ")
            ora = input("Dati ora tranzactiei")

            data = datetime.datetime.strptime(data, '%d-%m-%Y').date()
            ora = datetime.datetime.strptime(ora, '%H:%M').date()

            self.__tranzactieService.modifica(IdTranzactie, IdMedicament,
                                              IdCardClient, nrBucati,
                                              data, ora)
        except ValueError as ve:
            print(ve)
        except KeyError as ke:
            print(ke)
        except Exception as e:
            print(e)

    def showAllTranzactie(self):
        for tranzactie in self.__tranzactieService.getAll():
            print(tranzactie)

    def uiCautare(self):
        text = input("Dati textul pe care doriti sa il cautati: ")
        print(self.__tranzactieService.cautare(text))

    def uiTranzactiiIntervalDeZileDat(self):
        dataInceput = input("Dati data de inceput: ")
        dataSfarsit = input("Dati data de sfarsit: ")

        dataInceput = datetime.datetime.strptime(
            dataInceput, '%d-%m-%Y').date()
        dataSfarsit = datetime.datetime.strptime(
            dataSfarsit, '%d-%m-%Y').date()

        print(self.__tranzactieService.intervalTranzactii(dataInceput, dataSfarsit))

    def uiStergereTranzactiiIntervalDeZileDat(self):
        dataInceput = input("Dati data de inceput: ")
        dataSfarsit = input("Dati data de sfarsit: ")

        dataInceput = datetime.datetime.strptime(
            dataInceput, '%d-%m-%Y').date()
        dataSfarsit = datetime.datetime.strptime(
            dataSfarsit, '%d-%m-%Y').date()

        return self.__tranzactieService.stergereTranzactiiIntervalDeZileDat(
            dataInceput, dataSfarsit)

    def uiMedicamenteOrdonateDescrescatorDupaVanzari(self):
        for tranzactiePerMedicament in \
                self.__tranzactieService.medicamenteOrdonateDescrescatorDupaVanzari():
            print(tranzactiePerMedicament)

    def uiCarduriClientOrdonateDescrescatorDupaValoareaReducerilor(self):
        for tranzactiePerClient in \
                self.__tranzactieService.carduriClientOrdonateDescrescatorDupaValoareaReducerilor():
            print(tranzactiePerClient)

    def uiScumpireMedicament(self):
        procent = int(input("Dati un procent cu care se "
                            "scumpeste pretul medicamentului mai "
                            "mic decat valoarea data:"))
        valoare = int(input("Dati o valoare care trebuie comparata "
                            "cu pretul medicamnetelor: "))

        self.__tranzactieService.scumpireMedicamente(procent, valoare)

    def uiRandom(self):
        numeMedicamente = ["Ibuprofen", "Nurofen", "Alvocalmin",
                           "Emetrix", "Metoproclamid"]
        producator = ["Catena", "Secom", "OkMedical"]
        reteta = ["Da", "Nu"]
        n = int(input("Dati n: "))

        for i in range(n):
            medicament = random.choice(numeMedicamente)
            prod = random.choice(producator)
            pret = random.randint(10, 100)
            necesitaReteta = random.choice(reteta)
            id = str(i)

            self.__medicamentService.adauga(id, medicament,
                                            prod, pret, necesitaReteta)

    def uiStergereInCascada(self):
        print("sm. Stergere in cascada medicament")
        print("sc. Stergere in cascada card client")
        optiune = input("Dati optiunea: ")
        if optiune == "sm":
            IdMedicament = input("Dati Id-ul medicamentului "
                                 "care vreti sa il stergeti: ")
            self.__tranzactieService.stergereInCascadaMedicament(
                IdMedicament)
        elif optiune == "sc":
            IdCardClient = input("Dati Id-ul cardul client care "
                                 "vreti sa il stergeti: ")
            self.__tranzactieService.stergereInCascadaCardClient(
                IdCardClient)

    def runCRUDMedicamentMenu(self):
        print("1. Adauga medicament")
        print("2. Sterge medicament")
        print("3. Modifica medicament")
        print("4. Cautare medicament")
        print("a. Afiseaza toate medicamentele")
        print("x. Iesire")
        optiune = input("Dati optiunea: ")

        if optiune == "1":
            self.uiAdaugaMedicament()
        elif optiune == "2":
            self.uiStergeMedicament()
        elif optiune == "3":
            self.uiModificaMedicament()
        elif optiune == "4":
            self.uiCautareMedicament()
        elif optiune == "a":
            self.showAllMedicamente()
        else:
            print("Optiune gresita! Reincercati: ")
