from Domain.cardClient import CardClient


class CardClientViewModel:
    cardClient = CardClient
    valoareReducere = int

    def __init__(self, cardClient, valoareReducere):
        self.cardClient = cardClient
        self.valoareReducere = valoareReducere

    def __str__(self):
        return f'{self.cardClient} are reducerea {self.valoareReducere}'
