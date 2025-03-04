class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None

class ListaEnlazadaDoble:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def esta_vacia(self):
        return self.tamano == 0

    def agregar_al_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.cola
            self.cola.siguiente = nuevo_nodo
        self.cola = nuevo_nodo
        self.tamano += 1

    def obtener(self, indice):
        if indice < 0 or indice >= self.tamano:
            raise IndexError("Índice fuera de rango.")
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        return actual.dato

    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente