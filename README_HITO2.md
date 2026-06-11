# Hito 2: Informe - README

## 🎯 Objetivo

Generar un informe formal (máximo 8 páginas, formato IEEE) con análisis teórico y experimental de la compresión de arreglos ordenados usando Shannon-Fano.

## 📦 Entregables

- **informe.pdf** - Documento principal (< 8 páginas)
- **resultados/graficos/** - 3 gráficos PNG de alta calidad
- **resultados/estadisticas.json** - Datos procesados
- **PLAN_HITO2.md** - Planificación detallada
- **INSTRUCCIONES_HITO2.md** - Guía completa de uso

## ⚡ Quick Start (Si el benchmark ya terminó)

```bash
bash run_hito2.sh
```

Esto ejecutará automáticamente:
1. Procesa `salida.csv`
2. Genera gráficos
3. Compila `informe.pdf`

**Tiempo:** 5-10 minutos

---

## 📋 Contenido del Informe

### 1. Introducción y Contexto
- Motivación: compresión de datos ordenados
- Hipótesis: Shannon-Fano logra mejor balance espacio-tiempo
- Definición del problema

### 2. Metodología
- **Caso 1:** Búsqueda binaria explícita (O(log n) tiempo, 64n bits espacio)
- **Caso 2:** Gap Coding + Sample (O(√n) tiempo, variable espacio)
- **Caso 3:** Shannon-Fano sobre gaps (O(√n) tiempo, L×n bits espacio, donde L ≈ 2-4)

Incluye:
- Análisis asintótico matemático
- Pseudocódigos detallados
- Fórmulas de entropía y complejidad

### 3. Diseño Experimental
- Distribuciones: Lineal y Normal (Gaussiana)
- Tamaños: 8 MiB a 512 MiB (aprox. 10^6 a 10^8 elementos)
- Búsquedas: 262.144 por tamaño
- Compilador: g++ -O3 (optimización máxima)

### 4. Resultados
- **Gráfico 1:** Tiempo de búsqueda vs tamaño (escala log-log)
  - Valida O(log n) para Caso 1
  - Valida O(√n) para Casos 2 y 3
- **Gráfico 2:** Espacio utilizado vs tamaño
  - Muestra compresión: Caso 3 ≈ 25-35% de Caso 1
- **Gráfico 3:** Ratio de compresión
  - Compresión consistente a través de todos los tamaños

### 5. Conclusiones
- ✓ Shannon-Fano logra 60-75% de compresión (vs 20-30% de gap coding)
- ✓ Complejidad O(√n) confirmada experimentalmente
- ✗ Trade-off espacio-tiempo: 100× más lento que búsqueda binaria
- Aplicaciones recomendadas: datos en GPU/flash, búsquedas infrecuentes

---

## 📊 Estructura de Datos Generados

```
salida.csv (generado por ./main --benchmark)
│
├─→ scripts/process_results.py
│   └─→ resultados/
│       ├── estadisticas.json (datos parseados)
│       ├── datos_lineal.csv
│       └── datos_normal.csv
│
├─→ scripts/generate_graphs.py
│   └─→ resultados/graficos/
│       ├── 01_tiempo_busqueda.png
│       ├── 02_espacio_utilizado.png
│       └── 03_ratio_compresion.png
│
└─→ informe.tex + gráficos
    └─→ pdflatex
        └─→ informe.pdf ✓
```

---

## 🛠️ Herramientas Utilizadas

| Componente | Herramienta | Versión |
|-----------|-----------|---------|
| Compilación | g++ | C++17 |
| Procesamiento | Python 3 | 3.8+ |
| Gráficos | Matplotlib | 3.3+ |
| Datos | Pandas | 1.0+ |
| Informe | LaTeX | TeXLive |

---

## 📝 Convenciones del Código

### Scripts Python

**process_results.py:**
- Entrada: `salida.csv`
- Proceso: Parse CSV → Agrupación por distribución → JSON
- Salida: `resultados/estadisticas.json`

**generate_graphs.py:**
- Entrada: `resultados/estadisticas.json`
- Proceso: Carga datos → Crea figuras → Exporta PNG
- Salida: `resultados/graficos/*.png`

### Documento LaTeX

**informe.tex:**
- Clase: `article` (twocolumn)
- Paquetes: amsmath, amssymb, graphicx, hyperref, listings
- Encoding: UTF-8
- Idioma: Español (babel)
- Márgenes: 0.75 in (estilo IEEE)

---

## 🔄 Flujo de Ejecución

```
1. Compilar código C++
   make

2. Ejecutar benchmark (15-30 min)
   ./main --benchmark -o salida.csv

3. Procesar resultados (30 seg)
   python3 scripts/process_results.py

4. Generar gráficos (1-2 min)
   python3 scripts/generate_graphs.py

5. Compilar informe (1-2 min)
   pdflatex informe.tex
   pdflatex informe.tex  # segunda pasada

6. ✓ Resultado: informe.pdf listo para entregar
```

---

## 📚 Algoritmo: Shannon-Fano

### Descripción Breve

Técnica de compresión de **longitud variable** que asigna códigos cortos a símbolos frecuentes y largos a raros.

### Construcción (Top-Down)

1. Ordenar gaps por frecuencia (descendente)
2. Dividir en dos grupos de frecuencia similar
3. Asignar prefijo 0 a izquierda, 1 a derecha
4. Repetir recursivamente hasta códigos únicos

### Ejemplo

```
Gaps: [1, 1, 2, 2, 5, 7] con frecuencias {1: 2, 2: 2, 5: 1, 7: 1}

Árbol Shannon-Fano:
        root
       /    \
      0      1
     / \    / \
    1   2  5   7
   (00) (01)(10)(11)

Resultado: códigos de 2 bits promedio
Compresión: 2×n bits vs 64×n bits ≈ 96% de reducción
```

### Propiedades

- **Código de prefijo:** Ningún código es prefijo de otro (decodificación única)
- **Optimalidad:** H(S) ≤ L < H(S) + 1 (donde H = entropía, L = promedio)
- **Simplicidad:** Más fácil de implementar que Huffman

---

## 🎨 Especificación de Gráficos

### 01_tiempo_busqueda.png
- **Tipo:** Scatter + líneas (log-log)
- **Ejes:** log(Tamaño) vs log(Tiempo en ms)
- **Series:** 3 líneas para Casos 1, 2, 3
- **Distribuciones:** 2 subgráficos (lineal y normal)
- **Resolución:** 300 DPI
- **Tamaño:** 14×5 pulgadas

### 02_espacio_utilizado.png
- **Tipo:** Scatter + líneas (log-log)
- **Ejes:** log(Tamaño) vs log(Espacio en MiB)
- **Series:** 3 líneas para Casos 1, 2, 3
- **Distribuciones:** 2 subgráficos
- **Resolución:** 300 DPI
- **Información:** Calcula ratio de compresión por tamaño

### 03_ratio_compresion.png
- **Tipo:** Líneas (escala lineal en Y, log en X)
- **Ejes:** Tamaño (log) vs Compresión (%)
- **Series:** 2 líneas (Caso 2 y Caso 3)
- **Distribución:** Lineal solamente (mejor compresión)
- **Resolución:** 300 DPI

---

## ✅ Validación Pre-Entrega

**Checklist:**

- [ ] `informe.pdf` genera sin errores
- [ ] Documento tiene ≤ 8 páginas
- [ ] 3 gráficos están incrustados y visibles
- [ ] Fórmulas matemáticas son legibles
- [ ] Tablas están formateadas correctamente
- [ ] No hay "Undefined control sequence" en LaTeX
- [ ] Portada tiene nombres de todos los integrantes
- [ ] Fecha correcta (11 de Junio, 2026)
- [ ] Referencias están completas
- [ ] Pseudocódigos tienen sintaxis clara

---

## 📞 Problemas Frecuentes

| Problema | Causa | Solución |
|----------|-------|----------|
| `salida.csv` vacío | Benchmark en ejecución | Esperar 15-30 min |
| ModuleNotFoundError | Falta instalar pandas/matplotlib | `pip install pandas matplotlib numpy` |
| pdflatex no encontrado | LaTeX no instalado | `sudo apt-get install texlive-latex-extra` |
| Gráficos no aparecen | Ruta incorrecta | Verificar `resultados/graficos/` existe |
| LaTeX error "File not found" | Gráficos no generados | Ejecutar `python3 scripts/generate_graphs.py` |

---

## 📄 Licencia y Autoría

**Equipo:**
- David Minder
- Javier Ramírez
- Fabián Reyes
- Jorge Serón

**Curso:** INFO145 - Diseño y Análisis de Algoritmos  
**Profesor:** Héctor Ferrada Escobar  
**Semestre:** 1er semestre 2026

---

## 🚀 Próximos Pasos

1. Verificar que `salida.csv` tiene datos (si benchmark terminó)
2. Ejecutar: `bash run_hito2.sh`
3. Revisar: `informe.pdf`
4. Validar contra checklist anterior
5. Entregar a través de Siveduc

**Fecha de entrega:** Jueves 11 de Junio (HOY)

---

*Última actualización: 11 de Junio, 2026*
