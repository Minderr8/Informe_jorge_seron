# Instrucciones - Hito 2: Informe de Compresión

## 📋 Descripción General

Se ha creado un **pipeline automático** para generar el informe del Hito 2. El sistema comprende:

1. **Ejecución de benchmarks** (programa C++)
2. **Procesamiento de datos** (Python)
3. **Generación de gráficos** (Python + Matplotlib)
4. **Compilación de informe** (LaTeX → PDF)

---

## 🚀 Quick Start

### Opción 1: Ejecución Automática (Recomendado)

Si ya has ejecutado `./main --benchmark -o salida.csv`, simplemente:

```bash
bash run_hito2.sh
```

Este script hará todo automáticamente:
- ✓ Procesa el archivo `salida.csv`
- ✓ Genera gráficos en `resultados/graficos/`
- ✓ Compila `informe.pdf`

**Tiempo estimado:** 5-10 minutos

---

## 📊 Pipeline Detallado

### Paso 1: Generar Datos de Benchmark

**Comando:**
```bash
./main --benchmark -o salida.csv
```

**Salida:**
- `salida.csv`: Archivo con métricas para todos los tamaños y distribuciones
- `benchmark.log`: Log de ejecución

**Nota:** Este paso es el más lento (15-30 minutos dependiendo del hardware).

**Contenido de salida.csv:**

```
SETTINGS
RANDOM_BINARY_SEARCH_COUNT,262144

LINEAL_VECTOR
size_MiB,gen_time_ms,sort_time_ms,...,sf_search_time_ms,space_bits_compressed,space_bits_explicit
8,<time>,<time>,...,<time>,<bits>,<bits>
16,<time>,<time>,...,<time>,<bits>,<bits>
...

NORMAL_VECTOR
size_MiB,standard_deviation_sigma,gen_time_ms,...
8,10,<time>,...
8,20,<time>,...
...
```

---

### Paso 2: Procesar Resultados

**Comando:**
```bash
python3 scripts/process_results.py
```

**Qué hace:**
- Lee `salida.csv`
- Parsea secciones de distribución lineal y normal
- Calcula estadísticas
- Genera JSONs para gráficos

**Salidas:**
```
resultados/
├── estadisticas.json       # Datos procesados (estructura JSON)
├── datos_lineal.csv        # Datos extraídos (formato CSV)
└── datos_normal.csv
```

**Estructura de estadisticas.json:**

```json
{
  "lineal": {
    "sizes": [8, 16, 32, ...],
    "case1_time": [0.5, 1.2, 2.8, ...],
    "case2_time": [2.1, 5.3, 12.0, ...],
    "case3_time": [1.9, 4.8, 11.5, ...],
    "case1_space_bits": [67108864, ...],
    "case2_space_bits": [53687091, ...],
    "case3_space_bits": [16777216, ...]
  },
  "normal": {
    "sigma_10": { ... },
    "sigma_20": { ... },
    ...
  }
}
```

---

### Paso 3: Generar Gráficos

**Comando:**
```bash
python3 scripts/generate_graphs.py
```

**Qué hace:**
- Lee `resultados/estadisticas.json`
- Crea 3 gráficos PNG de alta calidad:
  - **01_tiempo_busqueda.png**: Tiempo vs tamaño (escala log-log)
  - **02_espacio_utilizado.png**: Espacio vs tamaño (escala log-log)
  - **03_ratio_compresion.png**: Compresión alcanzada vs tamaño

**Características:**
- Escala logarítmica (doble log) para visualizar O(log n) vs O(√n)
- Leyendas claras diferenciando los 3 casos
- Resolución 300 DPI (apta para impresión)
- Formato PNG compatible con LaTeX

**Salidas:**
```
resultados/graficos/
├── 01_tiempo_busqueda.png
├── 02_espacio_utilizado.png
└── 03_ratio_compresion.png
```

---

### Paso 4: Compilar Informe LaTeX

**Prerequisitos:**

Si no tienes LaTeX instalado:
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra
```

**Comando:**
```bash
pdflatex -interaction=nonstopmode informe.tex
pdflatex -interaction=nonstopmode informe.tex  # Segunda pasada
```

**Alternativa (automática):**
```bash
bash run_hito2.sh
```

**Salida:**
- `informe.pdf`: Documento final (< 8 páginas)

**Contenido del informe:**

1. **Portada y Abstract**
2. **Introducción** (hipótesis, contexto)
3. **Metodología** (3 secciones: Caso 1, 2, 3 con pseudocódigos y análisis asintótico)
4. **Resultados** (gráficos insertados, tablas, análisis)
5. **Conclusiones** (validación de hipótesis, hallazgos)
6. **Referencias**

---

## 📁 Archivos Creados/Modificados

### Nuevos Archivos:

```
PLAN_HITO2.md                  ← Plan documentado de ejecución
INSTRUCCIONES_HITO2.md         ← Este archivo
informe.tex                    ← Documento LaTeX (plantilla + contenido)
informe.pdf                    ← PDF compilado [ENTREGABLE]
run_hito2.sh                   ← Script de automatización

scripts/
├── process_results.py         ← Procesa CSV → JSON
└── generate_graphs.py         ← Genera gráficos

resultados/
├── estadisticas.json          ← Datos para gráficos
├── datos_lineal.csv           ← Subset de salida.csv
├── datos_normal.csv
└── graficos/
    ├── 01_tiempo_busqueda.png
    ├── 02_espacio_utilizado.png
    └── 03_ratio_compresion.png
```

### Archivos Existentes (sin cambios):

```
salida.csv                     ← Generado por ./main --benchmark
```

---

## ⚙️ Configuración y Personalización

### Modificar Tamaños de Prueba

**Ubicación:** `main.cpp` (en la sección de benchmark)

```cpp
// Línea aprox. 150-200
std::vector<size_t> test_sizes = {8, 16, 32, 64, 128, 256, 512};  // MiB
```

Edita los valores según necesites (más pequeños = ejecución más rápida).

### Modificar Desviaciones Estándar

**Ubicación:** `main.cpp` (configuración de distribución normal)

```cpp
std::vector<int> sigmas = {10, 20, 50, 100};
```

### Personalizar Gráficos

**Ubicación:** `scripts/generate_graphs.py`

```python
# Colores, fuentes, estilos (líneas 15-40)
matplotlib.rcParams['figure.figsize'] = (14, 5)
matplotlib.rcParams['font.size'] = 11
```

### Personalizar Informe LaTeX

**Ubicación:** `informe.tex`

Puedes modificar:
- Títulos y subtítulos (sección 1.1, 2.1, etc.)
- Texto de introducción/conclusiones
- Colores, fuentes, márgenes
- Agregar/remover secciones

---

## 🔍 Resolución de Problemas

### "salida.csv no encontrado"

**Causa:** No has ejecutado el benchmark aún.

**Solución:**
```bash
./main --benchmark -o salida.csv
# Espera a que termine (15-30 min)
```

### "ModuleNotFoundError: No module named 'pandas'"

**Causa:** Falta instalar dependencias Python.

**Solución:**
```bash
pip install pandas numpy matplotlib
```

### "pdflatex: command not found"

**Causa:** LaTeX no está instalado.

**Solución:**
```bash
sudo apt-get install texlive-latex-base texlive-latex-extra
```

### Los gráficos no aparecen en el PDF

**Causa:** La ruta a las imágenes es incorrecta o las imágenes no existen.

**Solución:**
```bash
# Verifica que existen:
ls -l resultados/graficos/

# Si no existen:
python3 scripts/generate_graphs.py
```

### LaTeX "Undefined control sequence" error

**Causa:** Encoding UTF-8 no configurado correctamente.

**Solución:**
```bash
# Agregado en informe.tex (ya presente):
\usepackage[utf-8]{inputenc}
\usepackage[spanish]{babel}
```

---

## 📈 Validación de Resultados

### Checklist de Calidad:

- [ ] `informe.pdf` existe y es legible
- [ ] Documento tiene ≤ 8 páginas (excluye portada si es necesario)
- [ ] 3 gráficos están insertados correctamente
- [ ] Fórmulas matemáticas se ven correctas
- [ ] No hay warnings en compilación LaTeX
- [ ] Tablas de datos son legibles
- [ ] Referencias están completas

### Métricas Esperadas:

**Distribución Lineal:**
- Caso 1: ~0.5-5 ms para búsqueda (O(log n))
- Caso 2: ~2-50 ms (O(√n))
- Caso 3: ~1.5-40 ms (O(√n) con mejor constante)
- Compresión Caso 3: 60-75%

**Distribución Normal:**
- Varía según σ
- Compresión mejor con σ pequeño
- Peor con σ muy grande

---

## 📋 Formato del Informe

### Estructura Requerida:

```
1. Portada (autor, título, fecha)
2. Introducción (contexto, hipótesis) [0.5 págs]
3. Metodología (análisis asintótico, pseudocódigos) [1.5 págs]
4. Resultados (gráficos, tablas, análisis) [3 págs]
5. Conclusiones (validación hipótesis, hallazgos) [0.5 págs]
6. Referencias [1 pág]

Total: ≤ 8 páginas
```

### Formato IEEE:

- Dos columnas
- Márgenes: 0.75 in
- Fuente: 11pt
- Espaciado: simple

---

## 🎯 Próximos Pasos

1. **Ahora:** Verificar que `salida.csv` está generado
2. **Luego:** Ejecutar `bash run_hito2.sh`
3. **Validar:** Revisar `informe.pdf`
4. **Entregar:** Subir PDF a Siveduc

---

## 📞 Support

Si encuentras problemas, revisa:
1. `PLAN_HITO2.md` - Planificación detallada
2. `benchmark.log` - Log de ejecución del programa C++
3. `/tmp/latex.log` - Log de compilación LaTeX

---

**Última actualización:** 11 de Junio, 2026  
**Estado:** ✓ Documentación completa
