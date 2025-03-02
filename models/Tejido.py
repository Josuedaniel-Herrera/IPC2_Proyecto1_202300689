class Tejido:
    def __init__(self, filas, columnas):
        if filas <= 0 or columnas <= 0:
            raise ValueError("Filas y columnas deben ser mayores a 0.")
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[None for _ in range(columnas)] for _ in range(filas)]

    def agregar_proteina(self, fila, columna, proteina):
        if not (0 <= fila < self.filas and 0 <= columna < self.columnas):
            raise ValueError("Posición fuera de rango.")
        self.matriz[fila][columna] = proteina

    def obtener_proteina(self, fila, columna):
        return self.matriz[fila][columna]