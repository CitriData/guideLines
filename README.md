# Documentación Protocolos de Actuación - DS

Este repositorio centraliza y documenta los **Protocolos de Actuación** técnicos implementados para asegurar la correcta gobernanza, procesamiento e intercambio de información dentro de nuestro espacio de datos compartidos.

El objetivo de estos protocolos es estandarizar los procedimientos operativos, garantizando que el ciclo de vida de los datos cumpla con los estándares de interoperabilidad, seguridad y calidad requeridos.

## Estructura del repositorio

```
guideLines/
├── staticPackages/          # Protocolo para paquetes de datos estáticos
│   ├── README.md            # Resumen del protocolo y checklist de verificación
│   ├── 01_SDM (Smart Data Model).md
│   ├── 02_Paquete de Datos.md
│   └── 03_CKAN (Laboratorio de datos).md
│
└── tools/                   # Scripts y herramientas de apoyo
    ├── README.md
    └── parquet_metadata.ipynb
```

## Tools

En el directorio [`tools/`](tools/) se irán incorporando los scripts y herramientas necesarias para el desarrollo de los paquetes del DS. Consulta su [README](tools/README.md) para ver el contenido disponible.

## Índice de Protocolos de Actuación

Actualmente, el catálogo de protocolos cuenta con los siguientes procedimientos oficiales:

### 1. Protocolo `staticPackages` (Empaquetamiento de Información Estática)

Este protocolo define las directrices obligatorias para la recopilación, estructuración, metadatado y compresión de todos los conjuntos de datos de naturaleza estática antes de su publicación o inclusión formal en el espacio de datos. El objetivo es que los datos históricos, de referencia o de actualización no frecuente (estáticos) se almacenen y transfieran bajo un formato unificado, facilitando su posterior consumo y descubrimiento por parte de los participantes autorizados.

El protocolo se articula en **tres pasos secuenciales** documentados en [`staticPackages/`](staticPackages/):

| Paso | Documento | Descripción |
|------|-----------|-------------|
| 1 | [01 · SDM](staticPackages/01_SDM%20(Smart%20Data%20Model).md) | Creación del Smart Data Model normalizado y su `schema.json`. |
| 2 | [02 · Paquete de Datos](staticPackages/02_Paquete%20de%20Datos.md) | Generación del `.parquet` y el `metadata_final.json` para el Data Space. |
| 3 | [03 · CKAN](staticPackages/03_CKAN%20(Laboratorio%20de%20datos).md) | Publicación de la entrada en el catálogo web (Laboratorio de datos). |

> Consulta el [README de staticPackages](staticPackages/README.md) para un resumen del protocolo completo y la checklist de verificación.
