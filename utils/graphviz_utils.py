from graphviz import Digraph

def visualizar_tejido(tejido, nombre_archivo):
    """
    Genera una imagen PNG de la matriz de tejido usando Graphviz.
    - tejido: Objeto de la clase Tejido.
    - nombre_archivo: Nombre base para el archivo de salida (sin extensión).
    """
    dot = Digraph(name=nombre_archivo, format='png', node_attr={'shape': 'plaintext'})
    
    # Crear tabla HTML-like
    tabla = '''<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0">\n'''
    for fila in tejido.matriz:
        tabla += "<TR>"
        for celda in fila:
            texto = celda.cadena if celda else "INERTE"
            color = "#F0F0F0"  # Gris claro
            tabla += f'<TD BGCOLOR="{color}">{texto}</TD>'
        tabla += "</TR>\n"
    tabla += "</TABLE>>"
    
    dot.node('matriz', tabla)
    dot.render(filename=nombre_archivo, cleanup=True)
    print(f"\033[92mGr├ífico generado: {nombre_archivo}.png\033[0m")