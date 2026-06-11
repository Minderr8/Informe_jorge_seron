#!/usr/bin/env python3
"""
Script simple para procesar resultados sin dependencias externas.
Solo usa librerías estándar de Python.
"""

import json
import csv
import os
from pathlib import Path

def parse_csv(csv_path):
    """Parsea salida.csv manualmente sin pandas."""

    with open(csv_path, 'r') as f:
        lines = f.readlines()

    # Buscar secciones
    lineal_idx = None
    normal_idx = None

    for i, line in enumerate(lines):
        if 'LINEAL_VECTOR' in line:
            lineal_idx = i
        elif 'NORMAL_VECTOR' in line:
            normal_idx = i

    data_lineal = []
    data_normal = []

    # Procesar sección lineal
    if lineal_idx is not None:
        # Saltar header y línea vacía
        header_idx = lineal_idx + 1
        header = lines[header_idx].strip().split(',')

        # Leer datos hasta NORMAL_VECTOR
        end_idx = normal_idx if normal_idx else len(lines)
        for i in range(header_idx + 2, end_idx):
            line = lines[i].strip()
            if line:
                values = line.split(',')
                if len(values) == len(header):
                    row = {header[j]: values[j] for j in range(len(header))}
                    data_lineal.append(row)

    # Procesar sección normal
    if normal_idx is not None:
        header_idx = normal_idx + 1
        header = lines[header_idx].strip().split(',')

        for i in range(header_idx + 2, len(lines)):
            line = lines[i].strip()
            if line:
                values = line.split(',')
                if len(values) == len(header):
                    row = {header[j]: values[j] for j in range(len(header))}
                    data_normal.append(row)

    return data_lineal, data_normal

def compute_statistics(data_lineal, data_normal):
    """Computa estadísticas a partir de datos parseados."""

    stats = {'lineal': {}, 'normal': {}}

    if data_lineal:
        sizes = []
        case1_times = []
        case2_times = []
        case3_times = []
        case1_bits = []
        case2_bits = []
        case3_bits = []

        for row in data_lineal:
            try:
                sizes.append(float(row['size_MiB']))
                case1_times.append(float(row['true_search_time_ms']))
                case2_times.append(float(row['gc_true_search_time_ms']))
                case3_times.append(float(row['sf_search_time_ms']))
                case1_bits.append(float(row['space_bits_explicit']))
                case2_bits.append(float(row['gc_total_bits']))
                case3_bits.append(float(row['space_bits_compressed']))
            except (KeyError, ValueError):
                continue

        stats['lineal'] = {
            'sizes': sizes,
            'case1_time': case1_times,
            'case2_time': case2_times,
            'case3_time': case3_times,
            'case1_space_bits': case1_bits,
            'case2_space_bits': case2_bits,
            'case3_space_bits': case3_bits,
        }

    if data_normal:
        # Agrupar por sigma
        by_sigma = {}
        for row in data_normal:
            try:
                sigma = row['standard_deviation_sigma']
                if sigma not in by_sigma:
                    by_sigma[sigma] = []
                by_sigma[sigma].append(row)
            except KeyError:
                continue

        for sigma, rows in by_sigma.items():
            sizes = []
            case1_times = []
            case2_times = []
            case3_times = []
            case1_bits = []
            case2_bits = []
            case3_bits = []

            for row in rows:
                try:
                    sizes.append(float(row['size_MiB']))
                    case1_times.append(float(row['true_search_time_ms']))
                    case2_times.append(float(row['gc_true_search_time_ms']))
                    case3_times.append(float(row['sf_search_time_ms']))
                    case1_bits.append(float(row['space_bits_explicit']))
                    case2_bits.append(float(row['gc_total_bits']))
                    case3_bits.append(float(row['space_bits_compressed']))
                except (KeyError, ValueError):
                    continue

            stats['normal'][f'sigma_{sigma}'] = {
                'sizes': sizes,
                'case1_time': case1_times,
                'case2_time': case2_times,
                'case3_time': case3_times,
                'case1_space_bits': case1_bits,
                'case2_space_bits': case2_bits,
                'case3_space_bits': case3_bits,
            }

    return stats

def main():
    csv_path = 'salida.csv'

    if not Path(csv_path).exists():
        print(f"Error: {csv_path} no encontrado.")
        return

    print("Procesando resultados de benchmark...")

    data_lineal, data_normal = parse_csv(csv_path)

    print(f"✓ Datos lineales: {len(data_lineal)} filas")
    print(f"✓ Datos normales: {len(data_normal)} filas")

    stats = compute_statistics(data_lineal, data_normal)

    os.makedirs('resultados', exist_ok=True)

    # Guardar JSON
    with open('resultados/estadisticas.json', 'w') as f:
        json.dump(stats, f, indent=2)

    # Guardar CSVs
    if data_lineal:
        with open('resultados/datos_lineal.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data_lineal[0].keys())
            writer.writeheader()
            writer.writerows(data_lineal)

    if data_normal:
        with open('resultados/datos_normal.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data_normal[0].keys())
            writer.writeheader()
            writer.writerows(data_normal)

    print("✓ Datos procesados y guardados en resultados/")

if __name__ == '__main__':
    main()
