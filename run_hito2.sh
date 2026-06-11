#!/bin/bash
# Script de automatización para Hito 2
# Genera benchmarks, procesa datos, crea gráficos y compila informe LaTeX

set -e

echo "======================================"
echo "HITO 2: AUTOMATIZACIÓN COMPLETA"
echo "======================================"
echo ""

# Fase 1: Verificar que salida.csv existe
echo "[1/5] Verificando datos de benchmark..."
if [ ! -f "salida.csv" ]; then
    echo "ERROR: salida.csv no encontrado. Ejecuta primero:"
    echo "  ./main --benchmark -o salida.csv"
    exit 1
fi
echo "✓ Archivo salida.csv encontrado"
echo ""

# Fase 2: Procesar resultados
echo "[2/5] Procesando resultados..."
mkdir -p resultados
python3 scripts/process_results.py
echo "✓ Datos procesados"
echo ""

# Fase 3: Generar gráficos
echo "[3/5] Generando gráficos..."
mkdir -p resultados/graficos
python3 scripts/generate_graphs.py
echo "✓ Gráficos generados"
echo ""

# Fase 4: Compilar LaTeX
echo "[4/5] Compilando informe LaTeX..."
if ! command -v pdflatex &> /dev/null; then
    echo "ADVERTENCIA: pdflatex no encontrado. Instala texlive-latex-base:"
    echo "  sudo apt-get install texlive-latex-base texlive-latex-extra"
else
    pdflatex -interaction=nonstopmode informe.tex > /tmp/latex.log 2>&1 || {
        echo "ERROR en compilación LaTeX. Ver /tmp/latex.log"
        tail -20 /tmp/latex.log
        exit 1
    }
    # Segunda pasada para referencias
    pdflatex -interaction=nonstopmode informe.tex > /tmp/latex.log 2>&1 || true
    echo "✓ Informe compilado: informe.pdf"
fi
echo ""

# Fase 5: Limpiar temporales
echo "[5/5] Limpiando archivos temporales..."
rm -f informe.aux informe.log informe.toc informe.out 2>/dev/null || true
echo "✓ Limpieza completada"
echo ""

echo "======================================"
echo "✓ HITO 2 COMPLETADO"
echo "======================================"
echo ""
echo "Archivos generados:"
echo "  - informe.pdf (documento principal)"
echo "  - resultados/estadisticas.json (datos procesados)"
echo "  - resultados/datos_lineal.csv"
echo "  - resultados/datos_normal.csv"
echo "  - resultados/graficos/ (gráficos PNG)"
echo ""
