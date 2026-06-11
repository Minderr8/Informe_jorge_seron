#!/usr/bin/env python3
"""
Script para procesar resultados de benchmark del proyecto de compresión.
Lee salida.csv y genera estadísticas y visualizaciones.
"""

import pandas as pd
import numpy as np
import json
import os
from pathlib import Path

def parse_benchmark_csv(csv_path):
    """
    Parsea el archivo CSV de benchmark generado por el programa C++.
    Retorna dos DataFrames: uno para distribución lineal, otro para normal.
    """

    with open(csv_path, 'r') as f:
        content = f.read()

    # Dividir por secciones
    lineal_start = content.find('LINEAL_VECTOR')
    normal_start = content.find('NORMAL_VECTOR')

    lineal_section = content[lineal_start:normal_start] if normal_start > 0 else content[lineal_start:]
    normal_section = content[normal_start:] if normal_start > 0 else ""

    # Procesar sección LINEAL_VECTOR
    lineal_lines = lineal_section.split('\n')[2:]  # Saltar cabecera
    lineal_lines = [l for l in lineal_lines if l.strip() and not l.startswith('NORMAL')]

    if lineal_lines:
        from io import StringIO
        df_lineal = pd.read_csv(StringIO('\n'.join(lineal_lines)))
    else:
        df_lineal = pd.DataFrame()

    # Procesar sección NORMAL_VECTOR
    normal_lines = normal_section.split('\n')[2:]  # Saltar cabecera
    normal_lines = [l for l in normal_lines if l.strip()]

    if normal_lines:
        from io import StringIO
        df_normal = pd.read_csv(StringIO('\n'.join(normal_lines)))
    else:
        df_normal = pd.DataFrame()

    return df_lineal, df_normal

def compute_statistics(df_lineal, df_normal):
    """
    Calcula estadísticas agregadas.
    """
    stats = {
        'lineal': {},
        'normal': {}
    }

    # Estadísticas para distribución lineal
    if not df_lineal.empty:
        stats['lineal'] = {
            'sizes': df_lineal['size_MiB'].tolist() if 'size_MiB' in df_lineal.columns else [],
            'case1_time': df_lineal['true_search_time_ms'].tolist() if 'true_search_time_ms' in df_lineal.columns else [],
            'case2_time': df_lineal['gc_true_search_time_ms'].tolist() if 'gc_true_search_time_ms' in df_lineal.columns else [],
            'case3_time': df_lineal['sf_search_time_ms'].tolist() if 'sf_search_time_ms' in df_lineal.columns else [],
            'case1_space_bits': (df_lineal['size_MiB'] * 1024 * 1024 * 8).tolist() if 'size_MiB' in df_lineal.columns else [],
            'case2_space_bits': df_lineal['gc_total_bits'].tolist() if 'gc_total_bits' in df_lineal.columns else [],
            'case3_space_bits': df_lineal['space_bits_compressed'].tolist() if 'space_bits_compressed' in df_lineal.columns else [],
        }

    # Estadísticas para distribución normal
    if not df_normal.empty:
        # Agrupar por sigma (desviación estándar)
        for sigma in df_normal['standard_deviation_sigma'].unique() if 'standard_deviation_sigma' in df_normal.columns else []:
            df_sigma = df_normal[df_normal['standard_deviation_sigma'] == sigma]
            stats['normal'][f'sigma_{sigma}'] = {
                'sizes': df_sigma['size_MiB'].tolist() if 'size_MiB' in df_sigma.columns else [],
                'case1_time': df_sigma['true_search_time_ms'].tolist() if 'true_search_time_ms' in df_sigma.columns else [],
                'case2_time': df_sigma['gc_true_search_time_ms'].tolist() if 'gc_true_search_time_ms' in df_sigma.columns else [],
                'case3_time': df_sigma['sf_search_time_ms'].tolist() if 'sf_search_time_ms' in df_sigma.columns else [],
                'case1_space_bits': (df_sigma['size_MiB'] * 1024 * 1024 * 8).tolist() if 'size_MiB' in df_sigma.columns else [],
                'case2_space_bits': df_sigma['gc_total_bits'].tolist() if 'gc_total_bits' in df_sigma.columns else [],
                'case3_space_bits': df_sigma['space_bits_compressed'].tolist() if 'space_bits_compressed' in df_sigma.columns else [],
            }

    return stats

def main():
    csv_path = 'salida.csv'

    if not Path(csv_path).exists():
        print(f"Error: {csv_path} no encontrado. Ejecuta primero: ./main --benchmark -o salida.csv")
        return

    print("Procesando resultados de benchmark...")

    df_lineal, df_normal = parse_benchmark_csv(csv_path)

    print(f"✓ Datos lineales cargados: {len(df_lineal)} filas")
    print(f"✓ Datos normales cargados: {len(df_normal)} filas")

    stats = compute_statistics(df_lineal, df_normal)

    # Crear directorio de resultados
    os.makedirs('resultados', exist_ok=True)

    # Guardar estadísticas en JSON
    with open('resultados/estadisticas.json', 'w') as f:
        json.dump(stats, f, indent=2)

    # Guardar DataFrames para referencia
    df_lineal.to_csv('resultados/datos_lineal.csv', index=False)
    df_normal.to_csv('resultados/datos_normal.csv', index=False)

    print("✓ Datos procesados y guardados en resultados/")
    print("\nArchivos generados:")
    print("  - resultados/estadisticas.json")
    print("  - resultados/datos_lineal.csv")
    print("  - resultados/datos_normal.csv")

if __name__ == '__main__':
    main()
