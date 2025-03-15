import xml.etree.ElementTree as ET
import os
from models.Experimento import Experimento
from models.Tejido import Tejido
from models.Proteina import Proteina

def cargar_experimentos_desde_xml(ruta):
    try:
        # Convertir a ruta absoluta
        ruta_absoluta = os.path.abspath(ruta)
        if not os.path.isfile(ruta_absoluta):
            raise FileNotFoundError(f"Archivo no encontrado: {ruta_absoluta}")
        
        tree = ET.parse(ruta_absoluta)
        root = tree.getroot()
        experimentos = []

        for exp_xml in root.findall('experimento'):
            # Validar nombre
            nombre = exp_xml.get('nombre')
            if not nombre:
                raise ValueError("Experimento sin atributo 'nombre'.")

            # Validar tejido
            tejido_xml = exp_xml.find('tejido')
            if tejido_xml is None:
                raise ValueError(f"Experimento '{nombre}' sin sección 'tejido'.")

            try:
                filas = int(tejido_xml.get('filas'))
                columnas = int(tejido_xml.get('columnas'))
            except (TypeError, ValueError):
                raise ValueError(f"Filas/columnas en '{nombre}' no son números válidos.")

            # Validar rejilla
            rejilla_xml = tejido_xml.find('rejilla')
            if rejilla_xml is None or not rejilla_xml.text:
                raise ValueError(f"Rejilla vacía en '{nombre}'.")

            rejilla = rejilla_xml.text.strip().split('\n')
            if len(rejilla) != filas:
                raise ValueError(f"Filas declaradas ({filas}) ≠ filas reales ({len(rejilla)}) en '{nombre}'.")

            # Crear tejido
            tejido = Tejido(filas, columnas)
            for i, fila in enumerate(rejilla):
                elementos = fila.strip().split()
                if len(elementos) != columnas:
                    raise ValueError(f"Fila {i+1} en '{nombre}' tiene {len(elementos)} columnas, se esperaban {columnas}.")
                for j, codigo in enumerate(elementos):
                    tejido.agregar_proteina(i, j, Proteina(codigo))

            # Validar parejas
            proteinas_xml = exp_xml.find('proteinas')
            if proteinas_xml is None:
                raise ValueError(f"Experimento '{nombre}' sin sección 'proteinas'.")

            parejas = []
            for pareja_xml in proteinas_xml.findall('pareja'):
                partes = pareja_xml.text.strip().split()
                if len(partes) != 2:
                    raise ValueError(f"Pareja inválida en '{nombre}': {pareja_xml.text}")
                parejas.append((Proteina(partes[0]), Proteina(partes[1])))

            # Obtener límite
            limite_xml = exp_xml.find('limite')
            limite = None
            if limite_xml is not None and limite_xml.text is not None:
                try:
                    limite = int(limite_xml.text.strip())
                except ValueError:
                    raise ValueError(f"Valor inválido para límite en experimento '{nombre}'.")

            # Crear experimento
            experimento = Experimento(nombre)
            experimento.tejido = tejido
            experimento.parejas = parejas
            experimento.limite = limite
            experimentos.append(experimento)

        return experimentos

    except Exception as e:
        raise ValueError(f"Error al procesar XML: {str(e)}")