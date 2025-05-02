# Script en python que genera archivos con las secuencias de ADN de distintos TF dado un archivo fasta y tsv.

import os
import csv

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

def leer_picos(peaks_path):
    """Lee el archivo de picos (TSV) y devuelve una lista de diccionarios con TF_name, start y end."""
    peaks_data = []
    try:
        with open(peaks_path, 'r', newline='') as file:
            lector = csv.DictReader(file, delimiter='\t')
            columnas_requeridas = {"TF_name", "Peak_start", "Peak_end"}

            if not columnas_requeridas.issubset(lector.fieldnames):
                print("Error: El archivo de picos no contiene los encabezados requeridos.")
                return []

            for i, fila in enumerate(lector):
                try:
                    tf_name = fila["TF_name"]
                    start = int(float(fila["Peak_start"]))  # Trunca el decimal
                    end = int(float(fila["Peak_end"]))      # Trunca el decimal
                    peaks_data.append({
                        "TF_name": tf_name,
                        "start": start,
                        "end": end
                    })
                except (ValueError, KeyError) as e:
                    print(f"Advertencia: Coordenadas inválidas o datos faltantes en la línea {i + 2}: {fila}")
                    continue
        return peaks_data
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de picos: {peaks_path}")
        return []

def extraer_secuencias(peaks_data, genoma): 
    """Agrupa las secuencias extraídas por TF_name en un diccionario."""
    secuencias_por_tf = {} # Diccionario vacio 
    largo_genoma = len(genoma) # Para futuras precauciones

    for i, peak in enumerate(peaks_data): # Extraccion de los valores
        tf = peak["TF_name"]
        start = peak["start"]
        end = peak["end"]
        if 0 <= start < end <= largo_genoma:# Validacion longitud
            secuencia = genoma[start:end] # Extraccion secuencia del genoma
            header = f"{tf}_peak{i+1}_{start}_{end}" # Encabezado para identificar secuencia
            if tf not in secuencias_por_tf: # Para no gastar memoria extra
                secuencias_por_tf[tf] = []
            secuencias_por_tf[tf].append((header, secuencia))
        else:
            print(f"Advertencia: Coordenadas fuera de rango para {tf}: {start}-{end}")
    return secuencias_por_tf

def guardar_fasta_por_tf(secuencias_por_tf, output_dir):
    """Guarda archivos FASTA separados por cada TF_name."""

    if not os.path.exists(output_dir): # Precaucion
        os.makedirs(output_dir)

    for tf, secuencias in secuencias_por_tf.items(): # Recorre diccionarios
        file_path = os.path.join(output_dir, f"{tf}.fa") # Ruta del archivo a crear
        try: # Precaucion permisos
            with open(file_path, 'w') as f:
                for header, secuencia in secuencias:
                    f.write(f">{header}\n")
                    f.write(f"{secuencia}\n")
        except IOError:
            print(f"Error al escribir el archivo: {file_path}")


def main():
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