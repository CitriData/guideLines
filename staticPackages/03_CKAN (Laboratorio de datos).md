> 06/06/2026

El siguiente paso es generar una entrada web en html, para ello necesitaremos crear la siguiente estructura de carpetas:
```text
../
|
|- index.html
|
|nombrePaquete/
	|- organization.png
	|- nombrePaquete.png
	|- nombrePaquete.json
```

Realmente solo será necesario construir la carpeta "nombrePaquete" con los archivos internos necesarios:
- **nombrePaquete.json**: se trata de _schema.json_ de los pasos anteriores con los siguientes cambios:
	- _"downloadUrl"_: campo que contiene la URL del dataset de prueba, generado con el DataHub y con LIMIT 50
	- _"dataProvider"_: campo con los metadatos del Data Space, importante comprobar que estos son correctos.
- **nombrePaquete.png**: imagen relacionada con el set de datos para adornar la sección.
- **organization.png** imagen sin fondo de la organización que oferta el set de datos.
- *index.html*: archivo local para generar la web html y ver el resultado final. Para visualizar los paquetes hay que añadir estos a la variable "_DATASET_SOURCES_".

## Observaciones
- en "_modelTag_" poner las mínimas, siempre en mayusculas siguiendo las siguientes reglas:
	- **Siempre**: UCO, ATDFIWARE
	- **según dataset**: temática (EJ: COMERCIO, PLAGAS...)
	- para **sensores**: tipo de comunicación (EJ: LORAWAN)
- La URL que ofertamos en este apartado de la web debe ser una copia del dataset ofertado pero limitandola a 50 registros, esto se hace desde el DataHub de la plataforma.
- En el apartado "_sources_": debemos poner las fuentes originales del dataset así como la entidad que las haya procesado si y solo si dicha entidad es distinta a la entidad que publica la oferta.