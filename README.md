# Documentación de Protocolos de Actuación - Espacio de Datos

Este repositorio centraliza y documenta los **Protocolos de Actuación** técnicos implementados para asegurar la correcta gobernanza, procesamiento e intercambio de información dentro de nuestro espacio de datos compartidos.

El objetivo de estos protocolos es estandarizar los procedimientos operativos, garantizando que el ciclo de vida de los datos cumpla con los estándares de interoperabilidad, seguridad y calidad requeridos.

## Índice de Protocolos de Actuación

Actualmente, el catálogo de protocolos cuenta con los siguientes procedimientos oficiales:

1. Protocolo staticPackages: Protocolo especializado en el empaquetamiento y estructuración de la información estática destinada a ser integrada en el espacio de datos.

## Detalle de los Protocolos

### 1. Protocolo `staticPackages` (Empaquetamiento de Información Estática)

Este protocolo define las directrices obligatorias para la recopilación, estructuración, metadado y compresión de todos los conjuntos de datos de naturaleza estática antes de su publicación o inclusión formal en el espacio de datos.

#### **Objetivo**

Asegurar que los datos históricos, de referencia o de actualización no frecuente (estáticos) se almacenen y transfieran bajo un formato unificado, facilitando su posterior consumo y descubrimiento por parte de los participantes autorizados.

#### **Flujo General de Actuación**
1. **Identificación y Limpieza**: Identificar los datasets estáticos y aplicar las reglas de limpieza y validación de esquemas predefinidas.
2. **Generación de Metadatos**: Enriquecer el paquete con un archivo de metadatos estandarizado (ej. en formato JSON-LD o YAML) que describa el origen, la licencia y la estructura del dato.
3. **Estructuración del Paquete**: Agrupar los recursos de datos en directorios específicos bajo la nomenclatura estipulada.
4. **Validación de Integridad**: Generar sumas de comprobación (checksums como SHA-256) para garantizar la inmutabilidad y seguridad del paquete durante la transferencia.
5. **Publicación**: Registrar e incluir el paquete estático dentro del catálogo del espacio de datos.

#### **Estructura Esperada del Paquete**
```text
📦 static-package-example/
├── 📄 metadata.json          # Metadatos del espacio de datos (DCAT, etc.)
├── 📂 data/                  # Carpeta contenedora de los datos puros (CSV, Parquet, JSON, etc.)
│   ├── dataset_1.csv
│   └── dataset_2.parquet
├── 📄 README.md              # Descripción del contenido de este paquete específico
└── 📄 checksum.sha256        # Archivo de verificación de integridad
