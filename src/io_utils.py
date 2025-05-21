"""
 Funciones auxiliares de escritura de archivos FASTA
 """

import os

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