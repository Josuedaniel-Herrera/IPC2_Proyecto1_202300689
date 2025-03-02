from utils.graphviz_utils import visualizar_tejido
from utils.pdf_utils import generar_pdf

class Experimento:
    def __init__(self, nombre):
        if not nombre:
            raise ValueError("El experimento debe tener un nombre.")
        self.nombre = nombre
        self.tejido = None
        self.parejas = []

    def ejecutar_directamente(self):
        if not self._validar_experimento():
            raise ValueError("Experimento incompleto o inválido.")
        
        visualizar_tejido(self.tejido, "inicial")
        generar_pdf("inicial.png", "inicial.pdf")

        while self._reaccionar_adyacentes():
            pass  # Procesar todas las reacciones

        visualizar_tejido(self.tejido, "final")
        generar_pdf("final.png", "final.pdf")
        self._mostrar_resultado()

    def ejecutar_paso_a_paso(self):
        if not self._validar_experimento():
            raise ValueError("Experimento incompleto o inválido.")
        
        paso = 1
        visualizar_tejido(self.tejido, f"paso_{paso}")
        generar_pdf(f"paso_{paso}.png", f"paso_{paso}.pdf")

        while True:
            reacciono = False
            for i in range(self.tejido.filas):
                for j in range(self.tejido.columnas):
                    if self._procesar_celda(i, j):
                        paso += 1
                        visualizar_tejido(self.tejido, f"paso_{paso}")
                        generar_pdf(f"paso_{paso}.png", f"paso_{paso}.pdf")
                        reacciono = True
                        break  # Una reacción por paso
                if reacciono:
                    break
            if not reacciono:
                break

        self._mostrar_resultado()

    def _validar_experimento(self):
        return self.tejido and self.parejas

    def _reaccionar_adyacentes(self):
        reacciono = False
        for i in range(self.tejido.filas):
            for j in range(self.tejido.columnas):
                if self._procesar_celda(i, j):
                    reacciono = True
        return reacciono

    def _procesar_celda(self, fila, col):
        proteina = self.tejido.obtener_proteina(fila, col)
        if not proteina:
            return False

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            x, y = fila + dx, col + dy
            if 0 <= x < self.tejido.filas and 0 <= y < self.tejido.columnas:
                vecina = self.tejido.obtener_proteina(x, y)
                if vecina and self._es_pareja_valida(proteina, vecina):
                    self.tejido.agregar_proteina(fila, col, None)
                    self.tejido.agregar_proteina(x, y, None)
                    return True
        return False

    def _es_pareja_valida(self, p1, p2):
        return any(
            (p1.cadena == a.cadena and p2.cadena == b.cadena) or 
            (p1.cadena == b.cadena and p2.cadena == a.cadena)
            for (a, b) in self.parejas
        )

    def _mostrar_resultado(self):
        total = self.tejido.filas * self.tejido.columnas
        inertes = sum(1 for fila in self.tejido.matriz for celda in fila if not celda)
        porcentaje = (inertes / total) * 100

        if 30 <= porcentaje <= 60:
            print("\n\033[92mMedicamento exitoso!\033[0m")
        elif porcentaje < 30:
            print("\n\033[93mMedicamento no efectivo.\033[0m")
        else:
            print("\n\033[91mMedicamento fatal!\033[0m")