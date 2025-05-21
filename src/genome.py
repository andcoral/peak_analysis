"""
 Funciones relacionadas con la lectura del genoma
 """

def cargar_genoma(fasta_path):
    """Carga el genoma desde un archivo FASTA y devuelve una única cadena de texto."""
    try:
        with open(fasta_path, 'r') as file:
            secuencia = '' # Para el genoma en linea
            for linea in file:
                if not linea.startswith('>'): # Ignora titulo
                    secuencia += linea.strip() # JUnta todo
        return secuencia
    except FileNotFoundError: # Comprobacion de existencia archivo
        print(f"Error: No se encontró el archivo FASTA: {fasta_path}")
        return None