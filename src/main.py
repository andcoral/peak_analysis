"""
Punto de entrada del programa
"""

def main():

    from genome import cargar_genoma
    from peaks import leer_picos
    from peaks import extraer_secuencias
    from io_utils import guardar_fasta_por_tf

    """Función principal que orquesta la ejecución del script."""
    # Rutas predefinidas para los archivos
    peaks_file = "../data/union_peaks_file.tsv"  # Ruta al archivo TSV de los picos
    genome_fasta = "../data/E_coli_K12_MG1655_U00096.3.txt"  # Ruta al archivo FASTA del genoma
    output_dir = "../results"  # Ruta al directorio de salida

    # Cargar el genoma
    genoma = cargar_genoma(genome_fasta)
    if genoma is None:
        return

    # Leer los datos de los picos
    picos = leer_picos(peaks_file)
    if not picos:
        return

    # Extraer las secuencias del genoma
    secuencias = extraer_secuencias(picos, genoma)

    # Guardar las secuencias en archivos FASTA
    guardar_fasta_por_tf(secuencias, output_dir)

    print("Proceso completado con éxito.")

if __name__ == "__main__":
    main()