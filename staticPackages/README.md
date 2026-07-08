# Protocolo de Actuación — Paquetes Estáticos

Este directorio recoge la documentación relativa al protocolo de actuación para los **paquetes de datos estáticos**: aquellos conjuntos de datos que no requieren actualización o cuya frecuencia de actualización es muy baja (1-2 veces al año).

El protocolo se divide en tres pasos secuenciales:

---

## Paso 1 · Smart Data Model (SDM)

Se crea el modelo de datos normalizado siguiendo el estándar [Smart Data Models](https://github.com/smart-data-models/dataModel.Agrifood). El punto de partida es la herramienta [Calculadora SDM](https://smartservice.es/SDM/), que genera el `schema.json` a partir del esquema de la plataforma analítica.

**Estructura mínima del SDM:**
```
nombrePaquete/
├── examples/
│   └── README.md
├── doc/
│   └── README.md
├── schema.json
├── notes.yaml
└── ADOPTERS.yaml
```

Los SDM se publican en [CitriData/dataModel.Agrifood](https://github.com/CitriData/dataModel.Agrifood).

---

## Paso 2 · Paquete de Datos

A partir del `schema.json` y los datos originales, se genera el paquete completo usando el cuaderno [`parquet_metadata.ipynb`](../tools/parquet_metadata.ipynb).

**Estructura del paquete:**
```
nombrePaquete/
├── data/
│   ├── data.csv (o .json)
│   └── data.parquet
├── doc/
│   ├── rsc/
│   └── doc.md / doc.pdf
├── schema.json
└── metadata_final.json
```

---

## Paso 3 · CKAN (Laboratorio de datos)

Se genera la entrada web en HTML para el catálogo de datos. Solo es necesario construir la carpeta del paquete con sus archivos y añadirlo a la variable `DATASET_SOURCES` del `index.html` local para previsualizar el resultado.

**Estructura:**
```
nombrePaquete/
├── organization.png
├── nombrePaquete.png
└── nombrePaquete.json
```

---

## ✅ Checklist de verificación

### Paso 1 — SDM

- [ ] `$id` apunta a la carpeta correcta del GitHub de CitriData.
- [ ] `description` está en **inglés**, ni demasiado extensa ni demasiado escueta y con su enlace al tipo correspondiente de schema.org.
- [ ] Se ha eliminado el campo `publication_policy`.
- [ ] `modelTags` contiene como mínimo: `UCO`, `ATDFIWARE` y la temática del dataset (en mayúsculas).
- [ ] Estructura de carpetas creada.
    - [ ] `examples/example-keyvalues.json` y `examples/README.md` creados.
    - [ ] `doc/README.md` creado con el formato standar de los [SDM](https://github.com/smart-data-models/dataModel.Agrifood/blob/master/AgriCrop/doc/spec_ES.md#agricrop-ngsi-ld-key-values-ejemplo).
    - [ ] `context.jsonld` creado.

### Paso 2 — Paquete de Datos

- [ ] Archivo `.parquet` generado correctamente.
- [ ] `metadata_final.json` generado a partir de `schema.json` + `data.parquet`.
- [ ] Atributos del dataset verificados: nombres, tipos y descripciones (con enlace a `schema.org/type`) y en inglés.
- [ ] Campo `provider` completo y correcto: `connector_endpoint`, `did`, `trust_issuer`.
- [ ] Se ha eliminado `publication_policy` del `metadata_final.json`.
- [ ] Documentación en `doc/` redactada en `.md` y exportada a `.pdf`.
- [ ] (si procede) Añadidos recursos adicionales a `doc/rsc`

### Paso 3 — CKAN

- [ ] `nombrePaquete.json` es el `schema.json` con los campos `downloadUrl` y `dataProvider` añadidos/verificados.
- [ ] `downloadUrl` apunta a la copia del dataset **limitada a 50 registros** (generada desde el DataHub).
- [ ] `dataProvider` contiene los metadatos correctos del Data Space.
- [ ] `modelTags` con los mínimos necesarios, siempre en mayúsculas (`UCO`, `ATDFIWARE` + temática).
- [ ] Imágenes `nombrePaquete.png` y `organization.png` (sin fondo) incluidas.
- [ ] En `sources` se incluye la fuente original y, si procede, la entidad procesadora (solo si es distinta al publicador).
