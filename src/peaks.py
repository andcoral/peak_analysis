"""
Funciones para procesar el archivo de picos
"""

import csv

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