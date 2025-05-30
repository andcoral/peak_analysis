"""
 Funciones auxiliares de escritura de archivos FASTA. A partir de diccionarios previamente creados, 
 genera un archivo por cada par de clave y valor.
 """

import os

def guardar_fasta_por_tf(secuencias_por_tf, output_dir): # Parametos: diccionario y ruta de salida
    """Guarda archivos FASTA separados por cada TF_name."""

    if not os.path.exists(output_dir): # Precaucion
        os.makedirs(output_dir) # Crea la carpeta de salida en caso de que no exista

    for tf, secuencias in secuencias_por_tf.items(): # Recorre diccionarios
        file_path = os.path.join(output_dir, f"{tf}.fa") # Ruta y nombre del archivo a crear
        try: # Precaucion permisos
            with open(file_path, 'w') as file:
                for header, secuencia in secuencias:
                    file.write(f">{header}\n")
                    file.write(f"{secuencia}\n")
        except IOError:
            print(f"Error al escribir el archivo: {file_path}")