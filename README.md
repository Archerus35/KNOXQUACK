# KnoxQuack

_KnoxQuack es proyecto en el cuál se pueden realizar busquedas de información sobre los lanzamientos de videojuegos, de manera que al introducir el nombre de un videojuego, el programa te devolvera la caratula de dicho juego, la información general de este y una pequeña aportación de reseñas positivas y negativas sobre este mismo, esto esta pensado para que el usuario sea consciente si realmente le merece la pena o no de adquirir dicho producto._

##  2. Obtención de los datos, limpieza y descripción 

##  3. Exploración y visualización de los datos 

De los datos almacenados podemos contar los siguientes registros:

* 11000 juegos 
* alrededor de 55000 reviews 
* alrededor de 40000 usuarios 

La información para cada juego se presenta en la página con la información disponible del juego:

![Captura desde 2023-03-12 16-34-37](https://user-images.githubusercontent.com/116188406/224555440-01e87d88-7149-4028-8e76-b732123bc4b5.png)

Para facilitar la exposición también se ha facilitado una tabla con el número de reviews hechas por un único usuario siempre 
que estas sean mayor a 5. Se ha decidido así porque el algoritmo trabaja mucho mejor cuantas más reviews se han hecho aunque 
no siempre da los mismos datos de afinidad ya que hay usuarios que tan solo puntúan los juegos que no le gustan con 0 u otros 
que puntúan con muchos 10. 

![Captura desde 2023-03-12 16-40-06](https://user-images.githubusercontent.com/116188406/224555713-bdafc0cc-fc26-4fce-a58e-d9687e826a72.png)

También se pueden ver directamente en la página las reviews que han hecho esos usuarios y de la exploración, como puede observarse en la 
captura de abajo, hay usuarios que puntuaron varias veces el mismo juego. No se trata en este caso de duplicados sino de reviews distintas
realizadas en fechas diferentes del mismo juego, probablemente por cambios de opinión o errores. Sería interesante arrojar más luz a este 
detalle y puede ser útil para otros modelos de ML pero no era necesario para el desarrollo del sistema de recomendación. 

![Captura desde 2023-03-12 16-40-06](https://user-images.githubusercontent.com/116188406/224555975-b6bcec95-8933-43b3-8190-b3696b6e180a.png)



##  4. Preparación de los datos para los algoritmos de Machine Learning 

Para el desarrollo de este sistema de recomendación hemos usado `spark` en su versíon `3.2.3` Este procedimiento puede verse en el cuaderno 
de [Google Colab](https://colab.research.google.com/drive/1GhP9Fg4NEvbYbyqJa-ggkU5qzY09ti5G) que también se adjunta en este proyecto en la carpeta `recommendation_model` serán necesarios los archivos `games.json` y `reviews_data.json`, disponibles en el datalake `metacritic_scrape`.

El cuaderno viene con todo el proceso de instalación y configuración para que `spark` funcione. Es necesario mencionar que el lenguaje nativo 
de`spark` es `java`:coffee:, por lo que para su uso en `python`:snake: se usa `pyspark`. Para que no de problemas esta librería debe 
instalarse en la misma versión que la de spark. Además también es necesario configurar las variables de entorno con las rutas a donde se encuentran
tanto `spark` como la máquina virtual de `java`, en este caso en su versión 8. También usaremos, la librería de spark `mlib` que viene preparada 
con multitud de algoritmos listos para ser usados. 

![Captura desde 2023-03-12 16-54-49](https://user-images.githubusercontent.com/116188406/224556412-3d224be7-7504-4205-86cf-d35084678ce8.png)

Con `spark` podemos convertir fácilmente y rápidamente nuestros archivos `json` en dataframes que se presentan en formatos tabulares. 

![Captura desde 2023-03-12 17-03-25](https://user-images.githubusercontent.com/116188406/224557015-9d43683b-79d3-48c3-8201-47702988c43e.png)

Podemos visualizar también los tipos de datos que tenemos en nuestro dataframe puede usarse `printSchema()` es importante usar esta función 
porque debemos asegurarnos que todo lo que le pasamos al algoritmo sean datos numéricos. 

![Captura desde 2023-03-12 17-04-11](https://user-images.githubusercontent.com/116188406/224557069-04935de9-8a8f-4f39-9838-fc0b22096dd0.png)

Seleccionamos los campos que vamos a necesitar para pasárselos al algoritmo para entrenamiento, al que le pasaremos los datos de las reviews `user_id`,
`game_id` y `score`

![Captura desde 2023-03-12 17-08-04](https://user-images.githubusercontent.com/116188406/224557358-9f363ebf-bc94-4386-8c0c-09578a2582fe.png)

Por último antes de pasar al entrenamiento nos aseguramos de que todos los datos que tenemos sean numéricos

![Captura desde 2023-03-12 17-10-23](https://user-images.githubusercontent.com/116188406/224557413-195dac18-a549-48cd-a677-82c1ed637183.png)


##  5. Entrenamiento del modelo y resultados 

Para este caso, se ha decidido utlizar un algoritmo de recomendación llamado `Alternating Least Squares` o `ALS` para los amigos. Este algoritmo realiza
como todos, operaciones de productos de matrices para tratar de estimar una puntuación y está pensado específicamente para usuarios, productos 
y puntuaciones. En un experimento realizado hace algunas semanas dio buenos resultados para los datos de puntuaciones de películas de imdb. Este 
algoritmo además es usado por grandes compañías como Netflix o Amazon entre otras. 

También se consideró el algoritmo `a priori` disponible en la librería de `apyori` de `python`, funcionaba bien para datos de cestas de la compra 
pero no hubo tiempo de probarlo, pues la implementación de este sistema se comió gran parte del tiempo de este proyecto. 

Para entrenar el modelo se le pasa el número máximo de iteraciones `maxIter`, parámetro de regularización `regParam`, `userCol` la columna 
que contiene los datos de usuario, `itemCol` la columna que contiene los datos de producto y por último la columna de puntuación, `ratingCol`
si los datos son númericos nuestro modeloy los datos no son aleatorios no dará errores. Esto último es importante según recoge la propia 
[documentación de spark para ALS](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.recommendation.ALS.html) en la 
que asegura que datos no deterministas pueden causar errores. 

![Captura desde 2023-03-12 17-28-55](https://user-images.githubusercontent.com/116188406/224558347-a65de9d8-5eb7-4384-8823-56a19ab3af12.png)

En este caso no tenemos una manera de asegurar que nuestros datos son correctos con datos de test de validación ya que los gustos personales
a fin de cuentas son arbitrarios y ni siquiera muchas veces los propios sistemas de recomendación de las grandes compañías aciertan. En realidad
estos algoritmos se basan casi siempre en la premisa de valorar que los usuarios compren, no tanto que les guste algo más o menos, también 
es importante tenerlo en cuenta. 


Para probar nuestro modelo realizamos una conversión de nuestros datos nombre de juegos a diccionario de python para facilitar su visualización, 
ya que lo que nos llegará en última instancia son los `game_id` junto con `user_id` de las recomendaciones para ese usuario. También realizamos 
un filtrado de juegos populares, ojo, no quiere decir que sean los que más les gustó al público sino los que tienen más puntuaciones. Luego 
ajustamos la columna de `user_id` con el id del usuario cuyas recomendaciones queramos conocer y aplicamos la función `transform` del modelo
para realizar las predicciones. Luego ordenaremos las predicciones por puntuación de mayor a menor y tomaremos solo 20 del total. 


![Captura desde 2023-03-12 17-44-59](https://user-images.githubusercontent.com/116188406/224559274-20271b57-aaa6-49a4-a661-41981d4f28fa.png)



Estas son las puntuaciones que tenía por ejemplo este usuario con 9984689


![Captura desde 2023-03-12 17-39-04](https://user-images.githubusercontent.com/116188406/224558906-21a16497-e535-4d1a-b5a2-03c9f380f1d7.png)

Y estas fueron las recomendaciones. Podemos ver que recomienda juegos similares

![Captura desde 2023-03-12 17-40-04](https://user-images.githubusercontent.com/116188406/224558948-39b5e9b5-3b54-4360-b1dd-5da1072d56c9.png)

Una vez realizado el modelo y comprobado que funciona es hora de guardarlo para integrarlo en nuestra aplicación. Este proceso es tan 
sencillo como ejecutar `model.save("nombre_deseado")`. Posteriormente se usará otra librería diferente para cargarlo. Esto genera una 
carpeta con los datos del modelo entrenado. 


##  6. Integración del modelo en la aplicación 

El modelo que hemos generado en el paso anterior, en nuestro caso, se encuentra en la carpeta `als_model` para cargarlo usamos una librería 
diferente `ALSModel` que puede ejcutar la función `load` para cargar el modelo que se encuentra nuestro proyecto. Para no realizar todo 
el proceso de golpe cada vez que se realizan recomendaciones hemos creado una clase que implementa el sistema de recomendación para 
así poder dejar algunos pasos precargados y solo cargar los que sean necesarios para determinar las recomendaciones de usuario. 

Con este mismo objetivo se ha separado también los juegos más populares `popular_games.csv` y los nombres de los juegos previamente para 
evitar muchas consultas a la base de datos, lo cual ralentiza muchísimo la aplicación. 

La clase utiliza:

* Un constructor para iniciar la sesión de Spark 
* Método para detener la sesión 
* Método para cargar los nombres de los juegos 
* Método para cargar el modelo 
* Método para cargar los juegos populares
* Método para realizar la predicción 
* Método para transformar los datos de salida de nuevo para evitar consultas reiteradas a la base de datos

![Captura desde 2023-03-12 18-02-49](https://user-images.githubusercontent.com/116188406/224560262-743ca77b-845f-4dcc-8992-bae33e5cb5af.png)

Estos serían los pasos a seguir 

![Captura desde 2023-03-12 18-06-10](https://user-images.githubusercontent.com/116188406/224560469-03f6e052-bd59-4015-8273-ccd935d1d613.png)

En la aplicación se cargan previamente:
* La sesión 
* El modelo 
* Los nombres de los juegos 
* Los juegos populares 

Y a la hora de recibir las recomendaciones se cargan:
* El ajuste de los datos
* La predicción o transformación del modelo 
* La transformación de los datos de salida

##  7. Aplicación de Procesamiento del Lenguaje Natural: Chatbot con dialog flow 

##  8. Aplicación Web: Dockerización y despliegue

Si bien ajustar las cosas para evitar que nuestra aplicación cargara demasiadas cosas desde la base de datos ha sido 
la parte más tediosa, resolver los problemas que pueden plantear las distintas versiones, la falta de disponibilidad en 
máquinas debian de java 8 o las versiones demasiado antiguas que venían en algunas imágenes de docker supusieron un 
día entero de pruebas y errores. La decisión final fue crear una imagen de docker partiendo de una imagen de ubuntu 
jammy, sistema en el que se realizó y funciona esta aplicación perfectamente. Una vez que se entiend docker es sencillo. 

Aunque el Dockerfile quedó al final un poco sucio con tanta depuración realiza:
* Instalación de `python3` con `pip` 
* pipenv - Se iba a usar y se usó en una prueba para obtener un `requirements.txt` fiable de la aplicación 
* streamlit - aunque se instala con `requirements.txt`
* Java 8 
* `Spark` en su versión `3.2.3`
* Definición de las variables de entorno `$JAVA_HOME` y `$SPARK_HOME` 
* Lo necesario también para instalar mongodb (Este paso es necesario para que la aplicación funcione)
* Definición de variables de mongodb(también necesario)
* Se define el entorno virtual en el proyecto 
* Se instalan los `requirements.txt`
* Se expone el puerto de `streamlit`
* Se ejecuta

![Captura desde 2023-03-12 18-06-10](https://user-images.githubusercontent.com/116188406/224561252-03d562d3-7907-4126-acf8-86a608977e48.png)

Para su despliegue en Streamlit Cloud fue ademaś necesario añadir un archivo `packages.txt` con la especificación del paquete de java 8 si no
se hacía Streamlit arroja una `JavaGatewayException`. 

Por último solo es necesario definir la url del cluster de mongodb en el archivo de producción y ponerla como está con `streamlit.secrets`

##  9. Conclusiones





## Comenzando 🚀

_Para comenzar a usar KnoxQuack se implementara un sencillo manual para que el usuario no se sienta desorientado a la hora de su uso._

## Despliegue 📦

_El despliegue de esta aplicación esta realizado en Streamlit._

## Construido con 🛠️

### FRONT

### BACK

* Python

## Servicio de despliegue utilizado 🖇️

_El servicio de despliegue usado para esta ocasión es Streamlit, debido a su guía y accesibilidad bien expuesta para el usuario de forma que se pueda subir y desplegar con mayor facilidad._

Link de la aplicación: https://aresonay-knoxquack-app-5jrn6s.streamlit.app/


## Autores ✒️

* Ismael Armada González
* Ángel Serón Márquez
