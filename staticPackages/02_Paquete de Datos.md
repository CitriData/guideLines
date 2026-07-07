> 06/06/2026

El siguiente paso es crear el paquete de datos a ofertar, para ello necesitamos:
- **schema.json** generado para el SDM
- script _generar_parquet.py_.
- script _generar_metadata.py_.
El paquete de datos se presentará con la siguiente estructura de carpetas:
```text
../nombrePaquete/
	|
	|- data/
	|    |-data.csv (o .json)
	|    |-data.parquet
	|
	|- doc/
	| 	 |- rsc/
	|	 |    |- *
	|	 | 
	|    |-doc.md
	|    |-doc.pdf
	|
	|- schema.json
	|- metadata_final.json
```

## Explicación estructura.
* **data**: Carpeta donde se guardaran los datos en el formato original (.csv, .json...) y en formato comprimido .parquet que se obtendrá con el script correspondiente.
* **doc**: Carpeta con toda la documentación e información acerca de los datos, sus fuentes de origen, observaciones, la metodología usada y los articulos/recursos que acompañen dicha documentación. Se escribirá la documentación en formato .md y en .pdf.
* **schema.json**: se trata del schema generado siguiendo el protocolo de los Smart Data Model (mismo que para el SDM).
* **metadata_final.json**: archivo de metadatos con información relativa al paquete de datos para el Data Space (connector id, provider, dataset,...) es generado con el script _generar_metadata.py_

## Metodología
Partimos del **schema.json** generado en el paso anterior y de los datos (**data.csv**):
1. Generamos el archivo _.parquet_ de los datos.
2. Generamos el archivo _metadata_final.json_ a partir del schema.json y data.parquet.
3. Comprobar el archivo _metadata_final.json_:
	1. Atributos del dataset correctos
		- Names
		- types
		- description (con enlace a schema.org/type)
	2. Campo **"provider"** con todos los datos del DS correctamente
		- connector_endpoint
		- did
		- trust_issuer
4. Eliminar _publication_policy_
