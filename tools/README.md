# Tools

En este directorio se irán incorporando los distintos scripts necesarios para la preparación y empaquetado de los datos destinados al espacio de datos.


## Contenido actual

| Herramienta | Descripción | Última actualización |
|---|---|---|
| `parquet_metadata.ipynb` | Cuaderno Jupyter para la generación de archivos `.parquet` y `metadata_final.json` a partir de los datos originales y del `schema.json` del SDM. | 08/07/2026 |


## Scripts incluidos en el cuaderno

- **`generar_parquet.py`**: convierte los datos originales (`.csv` / `.json`) al formato comprimido `.parquet`.
- **`generar_metadata.py`**: genera el archivo `metadata_final.json` con los metadatos del paquete para el Data Space, a partir del `schema.json` y del archivo `.parquet` generado.