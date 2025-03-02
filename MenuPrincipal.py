from estructuras.ListaEnlazadaDoble import ListaEnlazadaDoble
from models.Experimento import Experimento
from models.Tejido import Tejido
from models.Proteina import Proteina
from utils.xml_utils import cargar_experimentos_desde_xml
from utils.graphviz_utils import visualizar_tejido  # Importación correcta
import sys

class MenuPrincipal:
    def __init__(self):
        self.catalogo_experimentos = ListaEnlazadaDoble()
        self.experimento_actual = None

    def mostrar_menu_principal(self):
        while True:
            print("\n\033[1;36m--- MENÚ PRINCIPAL ---\033[0m")
            print("\033[93m1. Inicializar sistema\033[0m")
            print("\033[93m2. Cargar catálogo de experimentos\033[0m")
            print("\033[93m3. Desarrollar experimento\033[0m")
            print("\033[93m4. Mostrar datos del estudiante\033[0m")
            print("\033[93m5. Salir\033[0m")
            opcion = input("\033[94mSeleccione una opción: \033[0m")

            try:
                if opcion == "1":
                    self.inicializar_sistema()
                elif opcion == "2":
                    self.crear_catalogo()
                elif opcion == "3":
                    self.desarrollar_experimento()
                elif opcion == "4":
                    self.mostrar_datos_estudiante()
                elif opcion == "5":
                    print("\n\033[92mSaliendo del programa...\033[0m")
                    sys.exit(0)
                else:
                    print("\033[91mError: Opción inválida.\033[0m")
            except Exception as e:
                print(f"\n\033[91mError: {str(e)}\033[0m")

    def inicializar_sistema(self):
        self.catalogo_experimentos = ListaEnlazadaDoble()
        self.experimento_actual = None
        print("\n\033[92mSistema reiniciado correctamente.\033[0m")

    def crear_catalogo(self):
        ruta = input("\033[94mIngrese la ruta del archivo XML: \033[0m")
        try:
            experimentos = cargar_experimentos_desde_xml(ruta)
            for exp in experimentos:
                self.catalogo_experimentos.agregar_al_final(exp)
            print(f"\n\033[92mSe cargaron {len(experimentos)} experimento(s) exitosamente.\033[0m")
        except FileNotFoundError:
            print("\n\033[91mError: El archivo no existe.\033[0m")
        except ET.ParseError: # type: ignore
            print("\n\033[91mError: El archivo XML está mal formado.\033[0m")
        except ValueError as e:
            print(f"\n\033[91mError en datos: {str(e)}\033[0m")

    def desarrollar_experimento(self):
        print("\n\033[1;36m--- DESARROLLAR EXPERIMENTO ---\033[0m")
        print("\033[93m1. Cargar manualmente\033[0m")
        print("\033[93m2. Cargar del catálogo\033[0m")
        print("\033[93m3. Regresar\033[0m")
        opcion = input("\033[94mSeleccione una opción: \033[0m")

        if opcion == "1":
            self.cargar_experimento_manual()
        elif opcion == "2":
            self.cargar_experimento_del_catalogo()
        elif opcion == "3":
            return
        else:
            print("\033[91mError: Opción inválida.\033[0m")

    def cargar_experimento_manual(self):
        nombre = input("\033[94mIngrese el nombre del experimento: \033[0m")
        try:
            filas = int(input("\033[94mIngrese el número de filas: \033[0m"))
            columnas = int(input("\033[94mIngrese el número de columnas: \033[0m"))
            tejido = Tejido(filas, columnas)

            print("\n\033[1;36m--- REJILLA DE PROTEÍNAS ---\033[0m")
            for i in range(filas):
                for j in range(columnas):
                    proteina = input(f"Ingrese la proteína para la celda ({i}, {j}): ").strip()
                    tejido.agregar_proteina(i, j, Proteina(proteina))

            print("\n\033[1;36m--- PAREJAS DE PROTEÍNAS ---\033[0m")
            num_parejas = int(input("\033[94mIngrese el número de parejas: \033[0m"))
            parejas = []
            for _ in range(num_parejas):
                p1 = input("Proteína 1: ").strip()
                p2 = input("Proteína 2: ").strip()
                parejas.append((Proteina(p1), Proteina(p2)))

            experimento = Experimento(nombre)
            experimento.tejido = tejido
            experimento.parejas = parejas
            self.catalogo_experimentos.agregar_al_final(experimento)
            print("\n\033[92mExperimento creado y agregado al catálogo.\033[0m")

        except ValueError:
            print("\n\033[91mError: Datos inválidos.\033[0m")

    def cargar_experimento_del_catalogo(self):
        if self.catalogo_experimentos.esta_vacia():
            print("\n\033[91mError: El catálogo está vacío.\033[0m")
            return

        print("\n\033[1;36m--- ELIJA UN EXPERIMENTO ---\033[0m")
        for i, exp in enumerate(self.catalogo_experimentos):
            print(f"\033[93m{i + 1}. {exp.nombre}\033[0m")

        try:
            idx = int(input("\033[94mSeleccione un experimento: \033[0m")) - 1
            if idx < 0 or idx >= self.catalogo_experimentos.tamano:
                raise ValueError
            self.experimento_actual = self.catalogo_experimentos.obtener(idx)
            self.menu_modificar_ejecutar()
        except:
            print("\n\033[91mError: Selección inválida.\033[0m")

    def menu_modificar_ejecutar(self):
        while True:
            print("\n\033[1;36m--- OPCIONES DEL EXPERIMENTO ---\033[0m")
            print("\033[93m1. Modificar\033[0m")
            print("\033[93m2. Ejecutar\033[0m")
            print("\033[93m3. Regresar\033[0m")
            opcion = input("\033[94mSeleccione una opción: \033[0m")

            if opcion == "1":
                self.modificar_experimento()
            elif opcion == "2":
                self.menu_ejecucion()
            elif opcion == "3":
                break
            else:
                print("\033[91mError: Opción inválida.\033[0m")

    def modificar_experimento(self):
        print("\n\033[1;36m--- MODIFICAR EXPERIMENTO ---\033[0m")
        print("\033[93m1. Cambiar nombre\033[0m")
        print("\033[93m2. Modificar rejilla\033[0m")
        print("\033[93m3. Modificar parejas\033[0m")
        print("\033[93m4. Regresar\033[0m")
        opcion = input("\033[94mSeleccione una opción: \033[0m")

        if opcion == "1":
            nuevo_nombre = input("\033[94mNuevo nombre: \033[0m").strip()
            self.experimento_actual.nombre = nuevo_nombre
            print("\n\033[92mNombre actualizado.\033[0m")
        elif opcion == "2":
            self.modificar_rejilla()
        elif opcion == "3":
            self.modificar_parejas()
        elif opcion == "4":
            return
        else:
            print("\033[91mError: Opción inválida.\033[0m")

    def modificar_rejilla(self):
        print("\n\033[1;36m--- MODIFICAR REJILLA ---\033[0m")
        filas = self.experimento_actual.tejido.filas
        columnas = self.experimento_actual.tejido.columnas
        for i in range(filas):
            for j in range(columnas):
                nueva_proteina = input(f"Ingrese nueva proteína para ({i}, {j}): ").strip()
                self.experimento_actual.tejido.agregar_proteina(i, j, Proteina(nueva_proteina))
        print("\n\033[92mRejilla actualizada.\033[0m")

    def modificar_parejas(self):
        print("\n\033[1;36m--- MODIFICAR PAREJAS ---\033[0m")
        self.experimento_actual.parejas = []
        num_parejas = int(input("\033[94mNúmero de parejas: \033[0m"))
        for _ in range(num_parejas):
            p1 = input("Proteína 1: ").strip()
            p2 = input("Proteína 2: ").strip()
            self.experimento_actual.parejas.append((Proteina(p1), Proteina(p2)))
        print("\n\033[92mParejas actualizadas.\033[0m")

    def menu_ejecucion(self):
        while True:
            print("\n\033[1;36m--- OPCIONES DE EJECUCIÓN ---\033[0m")
            print("\033[93m1. Ejecutar directamente\033[0m")
            print("\033[93m2. Ejecutar paso a paso\033[0m")
            print("\033[93m3. Regresar\033[0m")
            opcion = input("\033[94mSeleccione una opción: \033[0m")

            if opcion == "1":
                self.experimento_actual.ejecutar_directamente()
                visualizar_tejido(self.experimento_actual.tejido, "final")  # Uso correcto
            elif opcion == "2":
                self.experimento_actual.ejecutar_paso_a_paso()
            elif opcion == "3":
                break
            else:
                print("\033[91mError: Opción inválida.\033[0m")
            
    def mostrar_datos_estudiante(self):
        print("\n\033[1;36m--- DATOS DEL ESTUDIANTE ---\033[0m")
        print("\033[93mNombre: [Tu nombre]")
        print("Carné: [Tu carné]")
        print("Curso: Introducción a la Programación y Computación 2")
        print("Carrera: Ingeniería en Ciencias y Sistemas\033[0m")

if __name__ == "__main__":
    MenuPrincipal().mostrar_menu_principal()