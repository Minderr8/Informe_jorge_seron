#!/usr/bin/env python3
"""
Genera gráficos en formato SVG sin dependencias externas.
SVG se puede convertir a PNG con ImageMagick o Inkscape.
"""

import json
import math
from pathlib import Path

def load_stats():
    """Carga estadísticas."""
    with open('resultados/estadisticas.json', 'r') as f:
        return json.load(f)

def crear_svg_tiempo():
    """Crea SVG con gráfico de tiempo."""

    stats = load_stats()
    width, height = 800, 600
    margin = 80

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        '<style>',
        'text { font-family: Arial; font-size: 12px; }',
        'line { stroke: #ccc; stroke-width: 1; }',
        'circle { stroke-width: 2; fill: white; }',
        '.title { font-size: 16px; font-weight: bold; }',
        '</style>',
    ]

    # Grid
    for i in range(0, width, 50):
        svg_lines.append(f'<line x1="{i}" y1="{margin}" x2="{i}" y2="{height-margin}" />')
    for i in range(margin, height-margin, 50):
        svg_lines.append(f'<line x1="{margin}" y1="{i}" x2="{width-margin}" y2="{i}" />')

    # Ejes
    svg_lines.append(f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="black" stroke-width="2"/>')
    svg_lines.append(f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="black" stroke-width="2"/>')

    # Título
    svg_lines.append(f'<text x="{width//2}" y="30" text-anchor="middle" class="title">Tiempo de Búsqueda vs Tamaño</text>')
    svg_lines.append(f'<text x="40" y="{height//2}" text-anchor="middle" transform="rotate(-90 40 {height//2})">Tiempo (ms)</text>')
    svg_lines.append(f'<text x="{width//2}" y="{height-20}" text-anchor="middle">Tamaño (MiB)</text>')

    # Datos (simplificado)
    if stats['lineal']['sizes']:
        sizes = stats['lineal']['sizes']
        times_c1 = stats['lineal']['case1_time']
        times_c3 = stats['lineal']['case3_time']

        # Escalar datos
        max_size = max(sizes)
        max_time = max(max(times_c1), max(times_c3))
        scale_x = (width - 2*margin) / max_size
        scale_y = (height - 2*margin) / max_time

        # Caso 1 (rojo)
        for i, (x, y) in enumerate(zip(sizes, times_c1)):
            px = margin + x * scale_x
            py = height - margin - y * scale_y
            svg_lines.append(f'<circle cx="{px}" cy="{py}" r="4" stroke="red" />')
            if i > 0:
                px_prev = margin + sizes[i-1] * scale_x
                py_prev = height - margin - times_c1[i-1] * scale_y
                svg_lines.append(f'<line x1="{px_prev}" y1="{py_prev}" x2="{px}" y2="{py}" stroke="red" stroke-width="2"/>')

        # Caso 3 (azul)
        for i, (x, y) in enumerate(zip(sizes, times_c3)):
            px = margin + x * scale_x
            py = height - margin - y * scale_y
            svg_lines.append(f'<circle cx="{px}" cy="{py}" r="4" stroke="blue" />')
            if i > 0:
                px_prev = margin + sizes[i-1] * scale_x
                py_prev = height - margin - times_c3[i-1] * scale_y
                svg_lines.append(f'<line x1="{px_prev}" y1="{py_prev}" x2="{px}" y2="{py}" stroke="blue" stroke-width="2"/>')

    # Leyenda
    svg_lines.append(f'<circle cx="{width-150}" cy="60" r="4" stroke="red" />')
    svg_lines.append(f'<text x="{width-130}" y="65">Caso 1: Búsqueda Binaria</text>')
    svg_lines.append(f'<circle cx="{width-150}" cy="90" r="4" stroke="blue" />')
    svg_lines.append(f'<text x="{width-130}" y="95">Caso 3: Shannon-Fano</text>')

    svg_lines.append('</svg>')

    return '\n'.join(svg_lines)

def crear_svg_espacio():
    """Crea SVG con gráfico de espacio."""

    stats = load_stats()
    width, height = 800, 600
    margin = 80

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        '<style>',
        'text { font-family: Arial; font-size: 12px; }',
        'line { stroke: #ccc; stroke-width: 1; }',
        'circle { stroke-width: 2; fill: white; }',
        '.title { font-size: 16px; font-weight: bold; }',
        '</style>',
    ]

    # Grid
    for i in range(0, width, 50):
        svg_lines.append(f'<line x1="{i}" y1="{margin}" x2="{i}" y2="{height-margin}" />')
    for i in range(margin, height-margin, 50):
        svg_lines.append(f'<line x1="{margin}" y1="{i}" x2="{width-margin}" y2="{i}" />')

    # Ejes
    svg_lines.append(f'<line x1="{margin}" y1="{height-margin}" x2="{width-margin}" y2="{height-margin}" stroke="black" stroke-width="2"/>')
    svg_lines.append(f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height-margin}" stroke="black" stroke-width="2"/>')

    # Título
    svg_lines.append(f'<text x="{width//2}" y="30" text-anchor="middle" class="title">Espacio Utilizado vs Tamaño</text>')
    svg_lines.append(f'<text x="40" y="{height//2}" text-anchor="middle" transform="rotate(-90 40 {height//2})">Espacio (MiB)</text>')
    svg_lines.append(f'<text x="{width//2}" y="{height-20}" text-anchor="middle">Tamaño (MiB)</text>')

    # Datos
    if stats['lineal']['sizes']:
        sizes = stats['lineal']['sizes']
        space_c1 = [b/(1024*1024*8) for b in stats['lineal']['case1_space_bits']]
        space_c3 = [b/(1024*1024*8) for b in stats['lineal']['case3_space_bits']]

        max_size = max(sizes)
        max_space = max(max(space_c1), max(space_c3))
        scale_x = (width - 2*margin) / max_size
        scale_y = (height - 2*margin) / max_space

        # Caso 1 (rojo)
        for i, (x, y) in enumerate(zip(sizes, space_c1)):
            px = margin + x * scale_x
            py = height - margin - y * scale_y
            svg_lines.append(f'<circle cx="{px}" cy="{py}" r="4" stroke="red" />')
            if i > 0:
                px_prev = margin + sizes[i-1] * scale_x
                py_prev = height - margin - space_c1[i-1] * scale_y
                svg_lines.append(f'<line x1="{px_prev}" y1="{py_prev}" x2="{px}" y2="{py}" stroke="red" stroke-width="2"/>')

        # Caso 3 (azul)
        for i, (x, y) in enumerate(zip(sizes, space_c3)):
            px = margin + x * scale_x
            py = height - margin - y * scale_y
            svg_lines.append(f'<circle cx="{px}" cy="{py}" r="4" stroke="blue" />')
            if i > 0:
                px_prev = margin + sizes[i-1] * scale_x
                py_prev = height - margin - space_c3[i-1] * scale_y
                svg_lines.append(f'<line x1="{px_prev}" y1="{py_prev}" x2="{px}" y2="{py}" stroke="blue" stroke-width="2"/>')

    # Leyenda
    svg_lines.append(f'<circle cx="{width-150}" cy="60" r="4" stroke="red" />')
    svg_lines.append(f'<text x="{width-130}" y="65">Caso 1: Explícito</text>')
    svg_lines.append(f'<circle cx="{width-150}" cy="90" r="4" stroke="blue" />')
    svg_lines.append(f'<text x="{width-130}" y="95">Caso 3: Shannon-Fano</text>')

    svg_lines.append('</svg>')

    return '\n'.join(svg_lines)

def main():
    print("Generando gráficos SVG...")

    Path('resultados/graficos').mkdir(parents=True, exist_ok=True)

    # Generar SVG
    svg_tiempo = crear_svg_tiempo()
    with open('resultados/graficos/01_tiempo_busqueda.svg', 'w') as f:
        f.write(svg_tiempo)
    print("✓ Generado: 01_tiempo_busqueda.svg")

    svg_espacio = crear_svg_espacio()
    with open('resultados/graficos/02_espacio_utilizado.svg', 'w') as f:
        f.write(svg_espacio)
    print("✓ Generado: 02_espacio_utilizado.svg")

    print("\n✓ Gráficos SVG generados")
    print("\nNota: Los SVG se pueden convertir a PNG con:")
    print("  convert -density 300 <archivo>.svg <archivo>.png")

if __name__ == '__main__':
    main()
