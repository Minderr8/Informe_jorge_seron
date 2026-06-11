#!/usr/bin/env python3
"""
Script para generar gráficos de resultados de benchmarks.
Crea visualizaciones de tiempo vs tamaño y espacio vs tamaño.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import json
from pathlib import Path

# Usar backend sin GUI
matplotlib.use('Agg')

def load_data():
    """Carga datos procesados desde JSON."""
    if not Path('resultados/estadisticas.json').exists():
        print("Error: resultados/estadisticas.json no encontrado. Ejecuta process_results.py primero.")
        return None

    with open('resultados/estadisticas.json', 'r') as f:
        return json.load(f)

def plot_tiempo_busqueda(stats):
    """Crea gráficos de tiempo vs tamaño."""

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfico 1: Distribución Lineal
    ax = axes[0]
    if stats['lineal']:
        lineal = stats['lineal']
        sizes = np.array(lineal['sizes'])
        case1_time = np.array(lineal['case1_time'])
        case2_time = np.array(lineal['case2_time'])
        case3_time = np.array(lineal['case3_time'])

        ax.loglog(sizes, case1_time, 'o-', label='Caso 1: Búsqueda Binaria', linewidth=2, markersize=6)
        ax.loglog(sizes, case2_time, 's-', label='Caso 2: Gap Coding', linewidth=2, markersize=6)
        ax.loglog(sizes, case3_time, '^-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=6)

        # Línea de referencia O(log n)
        n_ref = sizes
        logn_ref = np.log2(n_ref) / np.log2(sizes[0]) * case1_time[0] * 0.5
        ax.loglog(n_ref, logn_ref, '--', color='gray', alpha=0.5, label='O(log n) referencia')

        ax.set_xlabel('Tamaño del arreglo (MiB)', fontsize=11)
        ax.set_ylabel('Tiempo de búsqueda (ms)', fontsize=11)
        ax.set_title('Distribución Lineal: Tiempo vs Tamaño', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

    # Gráfico 2: Distribución Normal
    ax = axes[1]
    if stats['normal']:
        # Seleccionar la primera sigma para mostrar
        first_sigma = list(stats['normal'].keys())[0]
        normal = stats['normal'][first_sigma]
        sizes = np.array(normal['sizes'])
        case1_time = np.array(normal['case1_time'])
        case2_time = np.array(normal['case2_time'])
        case3_time = np.array(normal['case3_time'])

        ax.loglog(sizes, case1_time, 'o-', label='Caso 1: Búsqueda Binaria', linewidth=2, markersize=6)
        ax.loglog(sizes, case2_time, 's-', label='Caso 2: Gap Coding', linewidth=2, markersize=6)
        ax.loglog(sizes, case3_time, '^-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=6)

        ax.set_xlabel('Tamaño del arreglo (MiB)', fontsize=11)
        ax.set_ylabel('Tiempo de búsqueda (ms)', fontsize=11)
        ax.set_title(f'Distribución Normal (σ={first_sigma}): Tiempo vs Tamaño', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('resultados/graficos/01_tiempo_busqueda.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico generado: 01_tiempo_busqueda.png")
    plt.close()

def plot_espacio_utilizado(stats):
    """Crea gráficos de espacio vs tamaño."""

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfico 1: Distribución Lineal
    ax = axes[0]
    if stats['lineal']:
        lineal = stats['lineal']
        sizes = np.array(lineal['sizes'])
        case1_space = np.array(lineal['case1_space_bits']) / (1024*1024*8)  # convertir a MiB
        case2_space = np.array(lineal['case2_space_bits']) / (1024*1024*8)
        case3_space = np.array(lineal['case3_space_bits']) / (1024*1024*8)

        ax.loglog(sizes, case1_space, 'o-', label='Caso 1: Explícito', linewidth=2, markersize=6)
        ax.loglog(sizes, case2_space, 's-', label='Caso 2: Gap Coding', linewidth=2, markersize=6)
        ax.loglog(sizes, case3_space, '^-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=6)

        # Mostrar ratios de compresión
        for i, (s, c1, c3) in enumerate(zip(sizes, case1_space, case3_space)):
            ratio = (1 - c3/c1) * 100 if c1 > 0 else 0
            print(f"  Lineal n={s} MiB: Compresión Shannon-Fano = {ratio:.1f}%")

        ax.set_xlabel('Tamaño del arreglo (MiB)', fontsize=11)
        ax.set_ylabel('Espacio utilizado (MiB)', fontsize=11)
        ax.set_title('Distribución Lineal: Espacio vs Tamaño', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

    # Gráfico 2: Distribución Normal
    ax = axes[1]
    if stats['normal']:
        first_sigma = list(stats['normal'].keys())[0]
        normal = stats['normal'][first_sigma]
        sizes = np.array(normal['sizes'])
        case1_space = np.array(normal['case1_space_bits']) / (1024*1024*8)
        case2_space = np.array(normal['case2_space_bits']) / (1024*1024*8)
        case3_space = np.array(normal['case3_space_bits']) / (1024*1024*8)

        ax.loglog(sizes, case1_space, 'o-', label='Caso 1: Explícito', linewidth=2, markersize=6)
        ax.loglog(sizes, case2_space, 's-', label='Caso 2: Gap Coding', linewidth=2, markersize=6)
        ax.loglog(sizes, case3_space, '^-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=6)

        ax.set_xlabel('Tamaño del arreglo (MiB)', fontsize=11)
        ax.set_ylabel('Espacio utilizado (MiB)', fontsize=11)
        ax.set_title(f'Distribución Normal (σ={first_sigma}): Espacio vs Tamaño', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('resultados/graficos/02_espacio_utilizado.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico generado: 02_espacio_utilizado.png")
    plt.close()

def plot_ratio_compresion(stats):
    """Crea gráfico de ratio de compresión."""

    fig, ax = plt.subplots(figsize=(10, 6))

    if stats['lineal']:
        lineal = stats['lineal']
        sizes = np.array(lineal['sizes'])
        case1_space = np.array(lineal['case1_space_bits'])
        case2_space = np.array(lineal['case2_space_bits'])
        case3_space = np.array(lineal['case3_space_bits'])

        ratio_case2 = (1 - case2_space/case1_space) * 100
        ratio_case3 = (1 - case3_space/case1_space) * 100

        ax.plot(sizes, ratio_case2, 'o-', label='Caso 2: Gap Coding', linewidth=2, markersize=8)
        ax.plot(sizes, ratio_case3, 's-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=8)

        ax.set_xlabel('Tamaño del arreglo (MiB)', fontsize=12)
        ax.set_ylabel('Compresión (%)', fontsize=12)
        ax.set_title('Ratio de Compresión vs Tamaño (Distribución Lineal)', fontsize=13, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')

    plt.tight_layout()
    plt.savefig('resultados/graficos/03_ratio_compresion.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico generado: 03_ratio_compresion.png")
    plt.close()

def main():
    print("Generando gráficos...")

    stats = load_data()
    if stats is None:
        return

    # Crear directorio de gráficos
    Path('resultados/graficos').mkdir(parents=True, exist_ok=True)

    print("\nGenerando visualizaciones:")
    plot_tiempo_busqueda(stats)
    plot_espacio_utilizado(stats)
    plot_ratio_compresion(stats)

    print("\n✓ Todos los gráficos han sido generados en resultados/graficos/")

if __name__ == '__main__':
    main()
