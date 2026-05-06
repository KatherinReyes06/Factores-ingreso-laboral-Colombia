# Factores que determinan el ingreso laboral en Colombia

Análisis de los factores que influyen en el ingreso laboral de los colombianos usando datos de la Gran Encuesta Integrada de Hogares (GEIH) del DANE, correspondientes al primer semestre de 2025 (enero a junio).

## Objetivo

Identificar qué factores (nivel educativo, tipo de contrato, sector económico, sexo, zona geográfica, posición ocupacional, horas trabajadas y antigüedad) tienen mayor influencia en el ingreso laboral, y en qué medida.

## Datos

Los datos provienen de la GEIH 2025 del DANE. Se utilizaron dos tablas: Características generales y Ocupados, cruzadas por las llaves DIRECTORIO, SECUENCIA_P, ORDEN y HOGAR.

Fuente: [GEIH 2025 — DANE](https://microdatos.dane.gov.co/index.php/catalog/853)

## Herramientas

- Python (pandas, numpy, matplotlib, plotly)
- Google Colab

## Estructura del repositorio

| Archivo | Descripción |
|---------|-------------|
| Factores_que_determinan_...carga_y_limpieza.ipynb | Notebook 01: carga, exploración y limpieza de datos |
| Factores_que_determinan_...Análisis_exploratorio_(EDA).ipynb | Notebook 02: análisis exploratorio con visualizaciones |
| Coordenadas_Departamentos.xlsx | Coordenadas geográficas de los departamentos (DANE - DIVIPOLA) |
| DICCIONARIO_GEIH_2025.xlsx | Diccionario de variables de la GEIH 2025 |

## Principales hallazgos

1. **Nivel educativo** es el factor más determinante. Solo a partir del nivel tecnológico la mediana del ingreso supera el salario mínimo.
2. **Tipo de contrato:** quienes tienen contrato escrito indefinido ganan más del doble que quienes no tienen contrato. El 59% de los trabajadores no tiene contrato escrito.
3. **Sector económico:** 14 de 22 sectores tienen medianas iguales o inferiores al SMLV, y concentran el 78.7% de los trabajadores.
4. **Sexo:** la brecha general es de 1.7%, pero al controlar por nivel educativo aparecen brechas de hasta 45% en los niveles más bajos.
5. **Horas trabajadas:** influyen hasta la jornada legal (46 horas), después el ingreso se estanca.
6. **Antigüedad:** no tiene influencia significativa en el ingreso.

## Autora

Katherin Liceth Reyes Enciso
- [LinkedIn](https://www.linkedin.com/in/katherin-liceth-reyes-enciso-911b62186/)
- [GitHub](https://github.com/KatherinReyes06)
- [App streamlit](https://factores-ingreso-laboral-colombia.streamlit.app/)
