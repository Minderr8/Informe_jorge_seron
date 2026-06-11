#!/bin/bash
# Script para compilar informe.tex a PDF
# Proporciona 3 opciones diferentes

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Compilador de Informe LaTeX - Hito 2                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Opción 1: pdflatex local
if command -v pdflatex &> /dev/null; then
    echo "✓ pdflatex encontrado. Compilando..."
    pdflatex -interaction=nonstopmode informe.tex > /tmp/latex1.log 2>&1

    if [ $? -eq 0 ]; then
        echo "Compilando segunda pasada..."
        pdflatex -interaction=nonstopmode informe.tex > /tmp/latex2.log 2>&1

        if [ $? -eq 0 ]; then
            echo "✓ Compilación exitosa"
            ls -lh informe.pdf
            echo "✓ informe.pdf generado"
            exit 0
        fi
    fi

    echo "❌ Error en compilación. Ver logs:"
    tail -20 /tmp/latex2.log
    exit 1
fi

# Opción 2: Docker
if command -v docker &> /dev/null; then
    echo "✓ Docker encontrado. Usando MiKTeX en container..."
    docker run --rm -v $(pwd):/app miktex/miktex:latest \
        bash -c "cd /app && pdflatex -interaction=nonstopmode informe.tex && pdflatex -interaction=nonstopmode informe.tex"

    if [ $? -eq 0 ]; then
        echo "✓ Compilación exitosa con Docker"
        ls -lh informe.pdf
        exit 0
    fi
fi

# Opción 3: Instrucciones para Overleaf
echo "❌ pdflatex no encontrado. Instálalo o usa Overleaf:"
echo ""
echo "OPCIÓN A: Instalar LaTeX localmente"
echo "  Ubuntu/Debian:"
echo "    sudo apt-get install texlive-latex-base texlive-latex-extra"
echo ""
echo "  macOS:"
echo "    brew install --cask mactex"
echo ""
echo "OPCIÓN B: Usar Overleaf Online (RECOMENDADO)"
echo "  1. Abre https://www.overleaf.com"
echo "  2. New Project → Upload"
echo "  3. Sube informe.tex"
echo "  4. Haz clic en 'Recompile'"
echo "  5. Descarga el PDF"
echo ""
echo "OPCIÓN C: Docker"
echo "  docker run --rm -v \$(pwd):/app miktex/miktex:latest \\"
echo "    pdflatex -interaction=nonstopmode /app/informe.tex"
echo ""

exit 1
