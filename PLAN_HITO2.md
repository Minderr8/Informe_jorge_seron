# Plan de Ejecución - Hito 2: Informe

## Resumen General
Se generará un informe formal en LaTeX (máximo 8 páginas, formato IEEE) con análisis teórico y experimental del proyecto de compresión de arreglos ordenados.

**Algoritmo utilizado:** Shannon-Fano (Codificación de largo variable basada en frecuencias)

---

## Fases de Ejecución

### Fase 1: Compilación y Ejecución de Benchmarks
**Objetivo:** Obtener datos experimentales de rendimiento

**Pasos:**
1. Compilar el código C++ con `make clean && make`
2. Ejecutar benchmark: `./main --benchmark -o salida.csv`
3. Guardar los resultados en `salida.csv`

**Salida esperada:**
- Archivo CSV con métricas de:
  - Caso 1: Búsqueda binaria explícita (línea base)
  - Caso 2: Gap Coding con índice de muestreo
  - Caso 3: Shannon-Fano sobre gaps comprimidos
- Métricas: tiempo de generación, búsqueda, espacio utilizado

**Distribuciones a probar:**
- Distribución lineal: `A[i] = A[i-1] + rand() % ε`
- Distribución normal: múltiples desviaciones estándar

---

### Fase 2: Procesamiento de Datos
**Objetivo:** Parsear y preparar datos para análisis y gráficos

**Script Python:** `process_results.py`
- Lee `salida.csv`
- Extrae métricas de tiempo y espacio
- Calcula promedios, desviaciones estándar
- Genera estructuras de datos para ploteo

**Salidas:**
- JSON/pickle con datos procesados
- Estadísticas resumidas por distribución y tamaño

---

### Fase 3: Generación de Gráficos
**Objetivo:** Visualizar resultados experimentales

**Script Python:** `generate_graphs.py`
- Crea gráficos de tiempo vs tamaño (n)
- Crea gráficos de espacio vs tamaño (n)
- Compara los 3 casos
- Incluye líneas de tendencia teóricas si es aplicable

**Gráficos a generar:**
1. **Tiempo de búsqueda vs n** (lineal y normal)
   - 3 líneas: Caso 1, Caso 2, Caso 3
   - Escala logarítmica (doble log) para validar O(log n)

2. **Espacio utilizado vs n** (lineal y normal)
   - Comparación de MB utilizados
   - Ratio de compresión respecto a Caso 1

3. **Trade-off espacio-tiempo**
   - Tiempo de búsqueda vs bytes guardados
   - Análisis de Pareto

**Formato:** PNG/PDF de alta calidad, listos para LaTeX

---

### Fase 4: Análisis Teórico
**Objetivo:** Documentar complejidad asintótica y fórmulas

**Contenido a documentar:**

#### Caso 1 (Búsqueda Binaria)
- Complejidad: O(log n) tiempo de búsqueda
- Espacio: n × sizeof(int64_t) = n × 8 bytes
- Fórmula: Espacio = 64n bits

#### Caso 2 (Gap Coding + Sample)
- Complejidad tiempo:
  - Búsqueda en sample: O(log(n/√n)) = O(log n - 0.5 log n) = O(log n)
  - Decodificación secuencial: O(√n) en peor caso
  - Total: O(log n + √n) ≈ O(√n) para n grandes
- Espacio de gaps: E[bits_gap] × n
  - Máximo valor de gap depende de distribución
  - Lineal: max_gap ≈ ε
  - Normal: max_gap depende de σ
- Espacio de sample: √n × sizeof(int64_t)
- Fórmula total: bits_gap × n + 64√n bits

#### Caso 3 (Shannon-Fano sobre Gaps)
- Complejidad tiempo:
  - Búsqueda binaria en sample: O(log √n)
  - Decodificación con Shannon-Fano: O(√n × L̄)
    - L̄ = longitud promedio de código = H(gaps) + 1
    - H(gaps) = entropía de Shannon
  - Total: O(log n + √n × H)
- Espacio: bits por gap según frecuencia
  - Fórmula: bits_sf = Σ(freq[g] × len[g]) / total_gaps
  - Teórico: bits_sf ≤ H(gaps) + 1
  - Espacio total: bits_sf × n + overhead sample
- Entropía de Shannon: H = -Σ p(g) × log₂(p(g))

---

### Fase 5: Redacción del Informe LaTeX
**Objetivo:** Crear documento formal completo

**Estructura (máx. 8 páginas):**

```
1. Portada
   - Título del proyecto
   - Nombres del equipo
   - Fecha

2. Introducción (0.5 pág)
   - Contexto del problema
   - Importancia de compresión en datos
   - Hipótesis: "Shannon-Fano logra mejor balance espacio-tiempo que gap coding puro"

3. Metodología (1.5 págs)
   - 3.1: Descripción algoritmo Shannon-Fano
     - Concepto de código de largo variable
     - Construcción del árbol top-down
     - Tabla de codificación
   - 3.2: Análisis asintótico teórico
     - Complejidad tiempo para cada caso
     - Complejidad espacio (fórmulas matemáticas)
   - 3.3: Diseño experimental
     - Tamaños de entrada
     - Distribuciones probadas
     - Cantidad de búsquedas
     - Entorno: compilador, optimización (-O3)

4. Resultados (3 págs)
   - 4.1: Métricas de Espacio
     - Tabla con espacio ocupado por n
     - Gráfico: espacio vs n (lineal)
     - Ratio de compresión
   - 4.2: Métricas de Tiempo
     - Tabla con tiempos de búsqueda
     - Gráfico: tiempo vs n (log-log)
     - Validación de O(log n) vs O(√n)
   - 4.3: Trade-off Espacio-Tiempo
     - Gráfico: tiempo vs compresión
     - Análisis beneficio/costo

5. Conclusiones (0.5 pág)
   - Validación/refutación de hipótesis
   - Hallazgos principales
   - Aplicaciones y limitaciones
   - Trabajo futuro

6. Apéndices (opcionales, no contar en 8 págs)
   - A: Pseudocódigos
   - B: Tablas de datos crudos
```

---

### Fase 6: Compilación y Validación
**Objetivo:** Generar PDF final

**Acciones:**
1. Compilar con pdflatex: `pdflatex informe.tex`
2. Compilar referencias/índices si es necesario
3. Validar que no haya warnings críticos
4. Verificar que cumpla 8 páginas máximo

---

## Archivos a Crear/Modificar

### Nuevos archivos:
```
📁 PLAN_HITO2.md                      ← Este archivo (documentación)
📁 scripts/process_results.py          ← Procesa salida.csv
📁 scripts/generate_graphs.py          ← Genera gráficos PNG
📁 informe.tex                         ← Documento LaTeX principal
📁 informe.pdf                         ← PDF compilado (salida final)
📁 resultados/                         ← Directorio con datos procesados
│   ├── datos_procesados.json
│   └── graficos/
│       ├── tiempo_lineal.png
│       ├── tiempo_normal.png
│       ├── espacio_lineal.png
│       ├── espacio_normal.png
│       └── tradeoff.png
```

### Archivos existentes:
```
salida.csv                             ← Generado por ./main --benchmark
```

---

## Cronograma Estimado

| Fase | Estimación | Status |
|------|-----------|--------|
| 1. Compilación y benchmarks | 5-10 min | ⏳ Por hacer |
| 2. Procesamiento datos | 5 min | ⏳ Por hacer |
| 3. Generación gráficos | 10 min | ⏳ Por hacer |
| 4. Análisis teórico | 15 min | ⏳ Por hacer |
| 5. Redacción LaTeX | 30 min | ⏳ Por hacer |
| 6. Compilación final | 5 min | ⏳ Por hacer |
| **TOTAL** | **≈70 min** | ⏳ |

---

## Notas Importantes

- Los benchmarks pueden tomar tiempo si se prueban muchos tamaños (10^6 a 10^8)
- La salida CSV debe parsearse correctamente; si hay formato diferente, ajustar scripts
- Los gráficos deben ser claros y tener leyendas en español
- El LaTeX debe compilar sin errores; usar utf-8 para caracteres españoles
- Validar que las fórmulas matemáticas estén correctas antes de incluirlas

---

## Próximo Paso
→ Iniciar Fase 1: Compilación y ejecución de benchmarks
