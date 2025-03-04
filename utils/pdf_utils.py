from fpdf import FPDF

def generar_pdf(imagen_path, pdf_path):
    """
    Convierte una imagen PNG a PDF usando FPDF.
    - imagen_path: Ruta de la imagen PNG.
    - pdf_path: Ruta de salida para el PDF.
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.image(imagen_path, x=10, y=10, w=190)  # Ajusta el tamaño según necesidad
        pdf.output(pdf_path)
        print(f"\033[92mPDF generado: {pdf_path}\033[0m")
    except Exception as e:
        print(f"\033[91mError al generar PDF: {str(e)}\033[0m")