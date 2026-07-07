> 06/06/2026

La idea es seguir el estándar de los **Smart Data Model**, creando un paquete de información sobre los datos ofertados. La estructura que deben llevar los SDM es la siguiente [Enlace SDM](https://github.com/smart-data-models/dataModel.Agrifood/tree/master). Aunque se construirá inicialmente con la siguiente estructura mínima aceptable:
```text
../nombrePaquete/
	|
	|- examples/
	|    |-README.md
	|
	|- doc/
	|    |-README.md
	|
	|- schema.json
	|- notes.yaml
	|- ADOPTERS.yaml
```
Nuestros SDM se subirán en el siguiente [enlace](https://github.com/CitriData/dataModel.Agrifood). 
## Explicación estructura.
- **examples**: Carpeta dónde se subirá ejemplos livianos del paquete de datos ofertados. Irá acompañada de un _README.md_ dónde se explicarán brevemente los datos ofertados, formato en que se presenta, tipos de datos, descripción, mención a fuente de datos original...
- **doc**: Carpeta dónde se pondrá toda la documentación y especificaciones de los datos, así como su licencia de uso. Lo ideal es presentar esta información en formato .md y en distintos idiomas.
- **schema.json**: Esquema normalizado de los datos, donde se hará referencia al SDM publicado, metadatos relativos al espacio de datos y al proveedor, descripción del dataset y para cada uno de los campos su _tipo_, _descripción_ y enlace al modelo de ese tipo, se usará el estándar de [schema.org](https://schema.org/).
- **notes.yaml**: Notas pertinentes que necesite el consumidor de los datos.
- **ADOPTERS.yaml**: Lista descriptiva de los distintos consumidores del modelo de datos.

## Metodología
Lo primero será crear el archivo **schema.json** a partir del esquema de datos de la plataforma (_Catalogo de datos_) para ello se usará la siguiente herramienta: [Calculadora SDM](https://smartservice.es/SDM/).
1. Cargar _esquema.json_ de la plataforma en la herramienta y rellenar los campos pertinentes.
2. Comprobar:
	1. **$id**:  debe ser el enlace a la carpeta del SDM de nuestro GitHub.
	2. **description**: debe ser una descripción en inglés (no muy extensa pero tampoco muy escueta) sobre los datos.
	3. Quitar **publication_policy**
3. Generar estructura de carpetas con sus diferentes apartados.

### Ejemplo
```json
{
  "$schema": "http://json-schema.org/schema",
  "$schemaVersion": "0.0.1",
  "$id": "https://github.com/CitriData/dataModel.Agrifood/blob/main/AgriParcelNewPlantation/schema.json",
  "title": "Nuevas Plantaciones Palma del Río, Córdoba (España)",
  "modelTags": [
    "AgriParcelNewPlantation",
    "CitriData",
    "UCO",
    "ATDFIWARE"
  ],
  "description": "Modelo de datos diseñado para catalogar y monitorizar geográficamente parcelas agrícolas de nueva implantación del Término Municipal de Palma del Río, Córdoba (España). Año de carga 2023.",
  "type": "object",
  "allOf": [
    {
      "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/GSMA-Commons"
    },
    {
      "$ref": "https://smart-data-models.github.io/data-models/common-schema.json#/definitions/Location-Commons"
    },
    {
      "properties": {
        "type": {
          "type": "string",
          "description": "Property. NGSI Entity Type. It has to be AgriParcelNewPlantation.",
          "enum": [
            "AgriParcelNewPlantation"
          ]
        },
        "dateLoad": {
          "type": "string",
          "description": "Property. Model:'https://schema.org/Text'. Año de referencia valores"
        },
        "idClasifica": {
          "type": "string",
          "description": "Property. Model:'https://schema.org/Text'. Clasificación"
        },
        "idCobertura": {
          "type": "string",
          "description": "Property. Model:'https://schema.org/Text'. Cobertura"
        },
        "cambioUso": {
          "type": "string",
          "description": "Property. Model:'https://schema.org/Text'. Cambio de uso"
        },
        "dataProvider": {
          "type": "string",
          "description": "Property. Model:'https://schema.org/Text'. Proveedor del Dato"
        },
        "dataOwner": {
          "type": "string",
          "description": "Property. Model:'https://schema.org/Text'. Propietario del Dato"
        }
      }
    }
  ],
  "required": [
    "id",
    "type"
  ],
  "derivedFrom": "SDM Schema",
  "license": "CC BY 4.0 ES"
}
```