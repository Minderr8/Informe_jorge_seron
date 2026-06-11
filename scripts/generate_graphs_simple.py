#!/usr/bin/env python3
"""
Script simple para generar gráficos sin dependencias externas.
Usa matplotlib que está disponible.
"""

import json
import math
from pathlib import Path

# Intentar importar matplotlib
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("ERROR: matplotlib no disponible")

def load_stats():
    """Carga estadísticas desde JSON."""
    json_path = 'resultados/estadisticas.json'
    if not Path(json_path).exists():
        print(f"Error: {json_path} no encontrado")
        return None

    with open(json_path, 'r') as f:
        return json.load(f)

def plot_tiempo():
    """Genera gráfico de tiempo vs tamaño."""

    stats = load_stats()
    if not stats:
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Lineal
    ax = axes[0]
    if stats['lineal']['sizes']:
        sizes = stats['lineal']['sizes']
        c1_time = stats['lineal']['case1_time']
        c2_time = stats['lineal']['case2_time']
        c3_time = stats['lineal']['case3_time']

        ax.loglog(sizes, c1_time, 'o-', label='Caso 1: Búsqueda Binaria', linewidth=2, markersize=6)
        ax.loglog(sizes, c2_time, 's-', label='Caso 2: Gap Coding', linewidth=2, markersize=6)
        ax.loglog(sizes, c3_time, '^-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=6)

        ax.set_xlabel('Tamaño del arreglo (MiB)', fontsize=11)
        ax.set_ylabel('Tiempo de búsqueda (ms)', fontsize=11)
        ax.set_title('Distribución Lineal: Tiempo vs Tamaño', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

    # Normal
    ax = axes[1]
    if stats['normal']:
        first_sigma = list(stats['normal'].keys())[0]
        normal = stats['normal'][first_sigma]
        sizes = normal['sizes']
        c1_time = normal['case1_time']
        c2_time = normal['case2_time']
        c3_time = normal['case3_time']

        ax.loglog(sizes, c1_time, 'o-', label='Caso 1: Búsqueda Binaria', linewidth=2, markersize=6)
        ax.loglog(sizes, c2_time, 's-', label='Caso 2: Gap Coding', linewidth=2, markersize=6)
        ax.loglog(sizes, c3_time, '^-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=6)

        ax.set_xlabel('Tamaño del arreglo (MiB)', fontsize=11)
        ax.set_ylabel('Tiempo de búsqueda (ms)', fontsize=11)
        ax.set_title(f'Distribución Normal (σ={first_sigma}): Tiempo vs Tamaño', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('resultados/graficos/01_tiempo_busqueda.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico generado: 01_tiempo_busqueda.png")
    plt.close()

def plot_espacio():
    """Genera gráfico de espacio vs tamaño."""

    stats = load_stats()
    if not stats:
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Lineal
    ax = axes[0]
    if stats['lineal']['sizes']:
        sizes = stats['lineal']['sizes']
        c1_space = [b / (1024*1024*8) for b in stats['lineal']['case1_space_bits']]
        c2_space = [b / (1024*1024*8) for b in stats['lineal']['case2_space_bits']]
        c3_space = [b / (1024*1024*8) for b in stats['lineal']['case3_space_bits']]

        ax.loglog(sizes, c1_space, 'o-', label='Caso 1: Explícito', linewidth=2, markersize=6)
        ax.loglog(sizes, c2_space, 's-', label='Caso 2: Gap Coding', linewidth=2, markersize=6)
        ax.loglog(sizes, c3_space, '^-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=6)

        ax.set_xlabel('Tamaño del arreglo (MiB)', fontsize=11)
        ax.set_ylabel('Espacio utilizado (MiB)', fontsize=11)
        ax.set_title('Distribución Lineal: Espacio vs Tamaño', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

    # Normal
    ax = axes[1]
    if stats['normal']:
        first_sigma = list(stats['normal'].keys())[0]
        normal = stats['normal'][first_sigma]
        sizes = normal['sizes']
        c1_space = [b / (1024*1024*8) for b in normal['case1_space_bits']]
        c2_space = [b / (1024*1024*8) for b in normal['case2_space_bits']]
        c3_space = [b / (1024*1024*8) for b in normal['case3_space_bits']]

        ax.loglog(sizes, c1_space, 'o-', label='Caso 1: Explícito', linewidth=2, markersize=6)
        ax.loglog(sizes, c2_space, 's-', label='Caso 2: Gap Coding', linewidth=2, markersize=6)
        ax.loglog(sizes, c3_space, '^-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=6)

        ax.set_xlabel('Tamaño del arreglo (MiB)', fontsize=11)
        ax.set_ylabel('Espacio utilizado (MiB)', fontsize=11)
        ax.set_title(f'Distribución Normal (σ={first_sigma}): Espacio vs Tamaño', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('resultados/graficos/02_espacio_utilizado.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico generado: 02_espacio_utilizado.png")
    plt.close()

def plot_ratio():
    """Genera gráfico de ratio de compresión."""

    stats = load_stats()
    if not stats:
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    if stats['lineal']['sizes']:
        sizes = stats['lineal']['sizes']
        c1_space = stats['lineal']['case1_space_bits']
        c2_space = stats['lineal']['case2_space_bits']
        c3_space = stats['lineal']['case3_space_bits']

        ratio_c2 = [(1 - c2/c1)*100 for c1, c2 in zip(c1_space, c2_space)]
        ratio_c3 = [(1 - c3/c1)*100 for c1, c3 in zip(c1_space, c3_space)]

        ax.plot(sizes, ratio_c2, 'o-', label='Caso 2: Gap Coding', linewidth=2, markersize=8)
        ax.plot(sizes, ratio_c3, 's-', label='Caso 3: Shannon-Fano', linewidth=2, markersize=8)

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
    if not HAS_MATPLOTLIB:
        print("Matplotlib no disponible. Saltando generación de gráficos.")
        return

    print("Generando gráficos...")
    Path('resultados/graficos').mkdir(parents=True, exist_ok=True)

    plot_tiempo()
    plot_espacio()
    plot_ratio()

    print("\n✓ Todos los gráficos generados")

if __name__ == '__main__':
    main()
