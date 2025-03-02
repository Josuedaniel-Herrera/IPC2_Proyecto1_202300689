class Proteina:
    def __init__(self, cadena):
        if not cadena:
            raise ValueError("La cadena de aminoácidos no puede estar vacía.")
        self.cadena = cadena

    def __str__(self):
        return self.cadena