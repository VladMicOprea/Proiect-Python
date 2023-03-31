from dataclasses import dataclass


@dataclass
class MedicamentError(Exception):
    mesaj: any

    def __str__(self):
        return f'MedicamentError: {self.mesaj}'
