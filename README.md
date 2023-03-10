Proyecto patrocinado por:

<img src="https://raw.githubusercontent.com/MalagaTechPark/iabd-tfm-2223/main/malaga_tech_park.png" height="60px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://raw.githubusercontent.com/MalagaTechPark/iabd-tfm-2223/main/IABD_400.png" height="60px">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://raw.githubusercontent.com/MalagaTechPark/iabd-tfm-2223/main/accenture.svg" height="60px">


# 馃幃 KnoxQuack 馃

## Sistema de recomendaci贸n de videojuegos

![pato](https://user-images.githubusercontent.com/116188406/224566327-b77b0702-a616-4753-ad8c-1208481be215.jpg)

[Video explicando el sistema de recomendaci贸n](https://drive.google.com/file/d/1ZtnuXhJrD-VZCucKAaIZ9A2WQ-YfnbI6/view?usp=share_link)

## 1. Justificaci贸n y Descripci贸n 

_KnoxQuack es proyecto en el cu谩l se pueden realizar busquedas de informaci贸n sobre los lanzamientos de videojuegos, de manera que al introducir el nombre de un videojuego, el programa te devolvera la caratula de dicho juego, la informaci贸n general de este y una peque帽a aportaci贸n de rese帽as positivas y negativas sobre este mismo, esto esta pensado para que el usuario sea consciente si realmente le merece la pena o no de adquirir dicho producto._

##  2. Obtenci贸n de los datos, limpieza y descripci贸n 
<img src="https://upload.wikimedia.org/wikipedia/commons/4/48/Metacritic_logo.svg" alt="metacritic_logo" height="60px">

Los datos se han obtenido de la p谩gina web [metacritic](https://www.metacritic.com/browse/games/release-date/available/pc/metascore). Hemos 
decidido centrarnos para este proyecto en los juegos de pc y las reviews que realizan los usuarios. Aunque para mostrar los datos de juego 
hemos tomado tambi茅n el valor de puntuaci贸n de la cr铆tica, lo relevante en este proyecto son los datos de rese帽as de usuario, de las que se han 
tomado fundamentalmente las puntuaciones. 

Todos los tanto obtenidos como generados del procesamiento y la transformaci贸n para este proyecto, as铆 como los scripts de scraping que se 
han utilizado se encuentran en la carpeta `metacritic_scrape` que ejerce las funciones de data lake en nuestro proyecto. 

Para realizar la obtenci贸n de los datos, hemos dividido el proceso en dos pasos:
1. Obtenemos los datos de los juegos junto con las urls para las reviews 
2. A partir de las urls que hemos conseguido para las reviews, obtenemos tanto estas como los datos de usuarios

Se ha realizado as铆 para evitar realizar demasiadas peticiones de golpe, que el proceso demorase demasiado o que por alg煤n error falle 
todo a mitad del programa y despu茅s de esperar un mont贸n de tiempo te quedes sin nada. A alguien que conozco muy bien le pas贸 hace poco de hecho
El proceso se ha llevado a cabo con la librer铆a `BeautifulSoup` de `python`.

Para evitar tambi茅n hacer un proceso de limpieza de datos posterior, se han extremado las precauciones y se ha depurado conciezudamente para 
conseguir que los datos salgan lo m谩s limpios posibles y en un formato correcto para su manipulaci贸n. Para ello se han usado funciones para 
formatear fechas al formato usado en Espa帽a o para detectar los identificadores num茅ricos, limpiarlos de todo lo que no sea d铆gito y realizarle
un casteo para guardarlo en el formato debido. 


![Captura desde 2023-03-12 13-45-05](https://user-images.githubusercontent.com/116188406/224564714-a1392716-f145-4a9e-8cd9-695c0a3daf7a.png)


Era necesario configurar las cabeceras de las peticiones, que la url realizaba redirecciones, as铆 que hubo que hacer algunos 
ajustes para sortear ese problema

![Captura desde 2023-03-12 15-12-40](https://user-images.githubusercontent.com/116188406/224564849-095c7703-165e-45ea-a890-0c40b9821a07.png)

Solucionado el problema de las redirecciones ya pudimos iterar sobre las urls cogiendo los datos que busc谩bamos y almacen谩ndolos 

![Captura desde 2023-03-12 15-15-28](https://user-images.githubusercontent.com/116188406/224564934-88118596-895d-49cc-8863-ad51e7bb0c86.png)

Para los juegos hemos seleccionado los siguientes campos: 
* `game_id` - Identificador del juego tomado de su propio n煤mero en la p谩gina
* `title` - Titulo del juego 
* `description` - Descripci贸n del juego, est谩 en ingl茅s, del original
* `score` - Puntuaci贸n del juego otorgada por la cr铆tica especializada
* `date` - Fecha de lanzamiento 
* `img_url` - url de la imagen en la p谩gina para poder mostrarla en la aplicaci贸n 

Pudimos haber cogido todos los juegos, pero por precauci贸n seleccionamos 1100 juegos, muestra de datos m谩s que suficiente 
para poder llevar a cabo el algoritmo junto con los 55.000 registros de reviews. Una vez tomados y ordenados se escribieron 
al archivo `games.json`. Tambi茅 se escribe un archivo `reviews_urls.csv` con los datos de id del juego y la url de las reviews
relativas al juego, este archivo ser谩 el que lea el script `reviews_metacritic.py` para recoger los datos de las reviews. 

En el script `reviews_metacritic.py` se agregan unas funciones para crear un registro de usuario, el objetivo es comprobar 
si ese usuario existe en el registro, si no existe se le asigna un identificador que se extrae de una pila de n煤meros que 
empiezan desde los 10 millones hasta el 0 y se guarda en el registro, si el usuario ya existe simplemente se a帽ade su review 
y listo. 


![Captura desde 2023-03-12 15-34-55](https://user-images.githubusercontent.com/116188406/224565555-d7d0d43e-646a-4fb1-acb7-1254baf12f04.png)

Volvemos a realizar las iteraciones en busca de los datos y en este caso la ejecuci贸n demora m谩s, puesto que el script est谩 recogiendo m谩s 
datos que en el primer paso. 

![Captura desde 2023-03-12 15-42-10](https://user-images.githubusercontent.com/116188406/224565617-4addfa61-f681-45a7-8862-d62c4f54f28d.png)

Una vez terminado el proceso, se escriben, de nuevo dos archivos `reviews_data.json` en el que se recogen los datos de las reviews y 
el registro de usuarios `users_data.csv`  con los campso que se muestran a continuaci贸n:

Datos de reviews: 
* `username`- Nombre de usuario que realiz贸 la review
* `review_date` - Fecha en la que se realiz贸 la review
* `score`- Puntuaci贸n que le dio el usuario 
* `game_id` - Identificador del juego 
* `user_id`- Identificador de usuario

Datos de usuarios:
* `user_id` - Identificador de usuario
* `username` - Nombre de usuario

Estos datos se agregaron posteriormente al cluster de mongodb 


<img src="https://upload.wikimedia.org/wikipedia/commons/9/93/MongoDB_Logo.svg" height="60px">

##  3. Exploraci贸n y visualizaci贸n de los datos 

De los datos almacenados podemos contar los siguientes registros:

* 11000 juegos 
* alrededor de 55000 reviews 
* alrededor de 40000 usuarios 

La informaci贸n para cada juego se presenta en la p谩gina con la informaci贸n disponible del juego:

![Captura desde 2023-03-12 16-34-37](https://user-images.githubusercontent.com/116188406/224555440-01e87d88-7149-4028-8e76-b732123bc4b5.png)

Para facilitar la exposici贸n tambi茅n se ha facilitado una tabla con el n煤mero de reviews hechas por un 煤nico usuario siempre 
que estas sean mayor a 5. Se ha decidido as铆 porque el algoritmo trabaja mucho mejor cuantas m谩s reviews se han hecho aunque 
no siempre da los mismos datos de afinidad ya que hay usuarios que tan solo punt煤an los juegos que no le gustan con 0 u otros 
que punt煤an con muchos 10. 

![Captura desde 2023-03-12 16-40-06](https://user-images.githubusercontent.com/116188406/224555713-bdafc0cc-fc26-4fce-a58e-d9687e826a72.png)

Tambi茅n se pueden ver directamente en la p谩gina las reviews que han hecho esos usuarios y de la exploraci贸n, como puede observarse en la 
captura de abajo, hay usuarios que puntuaron varias veces el mismo juego. No se trata en este caso de duplicados sino de reviews distintas
realizadas en fechas diferentes del mismo juego, probablemente por cambios de opini贸n o errores. Ser铆a interesante arrojar m谩s luz a este 
detalle y puede ser 煤til para otros modelos de ML pero no era necesario para el desarrollo del sistema de recomendaci贸n. 

![Captura desde 2023-03-12 16-40-06](https://user-images.githubusercontent.com/116188406/224555975-b6bcec95-8933-43b3-8190-b3696b6e180a.png)



##  4. Preparaci贸n de los datos para los algoritmos de Machine Learning 

Para el desarrollo de este sistema de recomendaci贸n hemos usado `spark` en su vers铆on `3.2.3` Este procedimiento puede verse en el cuaderno 
de [Google Colab](https://colab.research.google.com/drive/1GhP9Fg4NEvbYbyqJa-ggkU5qzY09ti5G) que tambi茅n se adjunta en este proyecto en la carpeta `recommendation_model` ser谩n necesarios los archivos `games.json` y `reviews_data.json`, disponibles en el datalake `metacritic_scrape`.

El cuaderno viene con todo el proceso de instalaci贸n y configuraci贸n para que `spark` funcione. Es necesario mencionar que el lenguaje nativo 
de`spark` es `java`:coffee:, por lo que para su uso en `python`:snake: se usa `pyspark`. Para que no de problemas esta librer铆a debe 
instalarse en la misma versi贸n que la de spark. Adem谩s tambi茅n es necesario configurar las variables de entorno con las rutas a donde se encuentran
tanto `spark` como la m谩quina virtual de `java`, en este caso en su versi贸n 8. Tambi茅n usaremos, la librer铆a de spark `mlib` que viene preparada 
con multitud de algoritmos listos para ser usados. 

![Captura desde 2023-03-12 16-54-49](https://user-images.githubusercontent.com/116188406/224556412-3d224be7-7504-4205-86cf-d35084678ce8.png)

Con `spark` podemos convertir f谩cilmente y r谩pidamente nuestros archivos `json` en dataframes que se presentan en formatos tabulares. 

![Captura desde 2023-03-12 17-03-25](https://user-images.githubusercontent.com/116188406/224557015-9d43683b-79d3-48c3-8201-47702988c43e.png)

Podemos visualizar tambi茅n los tipos de datos que tenemos en nuestro dataframe puede usarse `printSchema()` es importante usar esta funci贸n 
porque debemos asegurarnos que todo lo que le pasamos al algoritmo sean datos num茅ricos. 

![Captura desde 2023-03-12 17-04-11](https://user-images.githubusercontent.com/116188406/224557069-04935de9-8a8f-4f39-9838-fc0b22096dd0.png)

Seleccionamos los campos que vamos a necesitar para pas谩rselos al algoritmo para entrenamiento, al que le pasaremos los datos de las reviews `user_id`,
`game_id` y `score`

![Captura desde 2023-03-12 17-08-04](https://user-images.githubusercontent.com/116188406/224557358-9f363ebf-bc94-4386-8c0c-09578a2582fe.png)

Por 煤ltimo antes de pasar al entrenamiento nos aseguramos de que todos los datos que tenemos sean num茅ricos

![Captura desde 2023-03-12 17-10-23](https://user-images.githubusercontent.com/116188406/224557413-195dac18-a549-48cd-a677-82c1ed637183.png)


##  5. Entrenamiento del modelo y resultados 

Para este caso, se ha decidido utlizar un algoritmo de recomendaci贸n llamado `Alternating Least Squares` o `ALS` para los amigos. Este algoritmo realiza
como todos, operaciones de productos de matrices para tratar de estimar una puntuaci贸n y est谩 pensado espec铆ficamente para usuarios, productos 
y puntuaciones. En un experimento realizado hace algunas semanas dio buenos resultados para los datos de puntuaciones de pel铆culas de imdb. Este 
algoritmo adem谩s es usado por grandes compa帽铆as como Netflix o Amazon entre otras. 

Tambi茅n se consider贸 el algoritmo `a priori` disponible en la librer铆a de `apyori` de `python`, funcionaba bien para datos de cestas de la compra 
pero no hubo tiempo de probarlo, pues la implementaci贸n de este sistema se comi贸 gran parte del tiempo de este proyecto. 

Para entrenar el modelo se le pasa el n煤mero m谩ximo de iteraciones `maxIter`, par谩metro de regularizaci贸n `regParam`, `userCol` la columna 
que contiene los datos de usuario, `itemCol` la columna que contiene los datos de producto y por 煤ltimo la columna de puntuaci贸n, `ratingCol`
si los datos son n煤mericos nuestro modeloy los datos no son aleatorios no dar谩 errores. Esto 煤ltimo es importante seg煤n recoge la propia 
[documentaci贸n de spark para ALS](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.recommendation.ALS.html) en la 
que asegura que datos no deterministas pueden causar errores. 

![Captura desde 2023-03-12 17-28-55](https://user-images.githubusercontent.com/116188406/224558347-a65de9d8-5eb7-4384-8823-56a19ab3af12.png)

En este caso no tenemos una manera de asegurar que nuestros datos son correctos con datos de test de validaci贸n ya que los gustos personales
a fin de cuentas son arbitrarios y ni siquiera muchas veces los propios sistemas de recomendaci贸n de las grandes compa帽铆as aciertan. En realidad
estos algoritmos se basan casi siempre en la premisa de valorar que los usuarios compren, no tanto que les guste algo m谩s o menos, tambi茅n 
es importante tenerlo en cuenta. 


Para probar nuestro modelo realizamos una conversi贸n de nuestros datos nombre de juegos a diccionario de python para facilitar su visualizaci贸n, 
ya que lo que nos llegar谩 en 煤ltima instancia son los `game_id` junto con `user_id` de las recomendaciones para ese usuario. Tambi茅n realizamos 
un filtrado de juegos populares, ojo, no quiere decir que sean los que m谩s les gust贸 al p煤blico sino los que tienen m谩s puntuaciones. Luego 
ajustamos la columna de `user_id` con el id del usuario cuyas recomendaciones queramos conocer y aplicamos la funci贸n `transform` del modelo
para realizar las predicciones. Luego ordenaremos las predicciones por puntuaci贸n de mayor a menor y tomaremos solo 20 del total. 


![Captura desde 2023-03-12 17-44-59](https://user-images.githubusercontent.com/116188406/224559274-20271b57-aaa6-49a4-a661-41981d4f28fa.png)



Estas son las puntuaciones que ten铆a por ejemplo este usuario con 9984689


![Captura desde 2023-03-12 17-39-04](https://user-images.githubusercontent.com/116188406/224558906-21a16497-e535-4d1a-b5a2-03c9f380f1d7.png)

Y estas fueron las recomendaciones. Podemos ver que recomienda juegos similares

![Captura desde 2023-03-12 17-40-04](https://user-images.githubusercontent.com/116188406/224558948-39b5e9b5-3b54-4360-b1dd-5da1072d56c9.png)

Una vez realizado el modelo y comprobado que funciona es hora de guardarlo para integrarlo en nuestra aplicaci贸n. Este proceso es tan 
sencillo como ejecutar `model.save("nombre_deseado")`. Posteriormente se usar谩 otra librer铆a diferente para cargarlo. Esto genera una 
carpeta con los datos del modelo entrenado. 


##  6. Integraci贸n del modelo en la aplicaci贸n 

El modelo que hemos generado en el paso anterior, en nuestro caso, se encuentra en la carpeta `als_model` para cargarlo usamos una librer铆a 
diferente `ALSModel` que puede ejcutar la funci贸n `load` para cargar el modelo que se encuentra nuestro proyecto. Para no realizar todo 
el proceso de golpe cada vez que se realizan recomendaciones hemos creado una clase que implementa el sistema de recomendaci贸n para 
as铆 poder dejar algunos pasos precargados y solo cargar los que sean necesarios para determinar las recomendaciones de usuario. 

Con este mismo objetivo se ha separado tambi茅n los juegos m谩s populares `popular_games.csv` y los nombres de los juegos previamente para 
evitar muchas consultas a la base de datos, lo cual ralentiza much铆simo la aplicaci贸n. 

La clase utiliza:

* Un constructor para iniciar la sesi贸n de Spark 
* M茅todo para detener la sesi贸n 
* M茅todo para cargar los nombres de los juegos 
* M茅todo para cargar el modelo 
* M茅todo para cargar los juegos populares
* M茅todo para realizar la predicci贸n 
* M茅todo para transformar los datos de salida de nuevo para evitar consultas reiteradas a la base de datos

![Captura desde 2023-03-12 18-02-49](https://user-images.githubusercontent.com/116188406/224560262-743ca77b-845f-4dcc-8992-bae33e5cb5af.png)

Estos ser铆an los pasos a seguir 

![Captura desde 2023-03-12 18-06-10](https://user-images.githubusercontent.com/116188406/224560469-03f6e052-bd59-4015-8273-ccd935d1d613.png)

En la aplicaci贸n se cargan previamente:
* La sesi贸n 
* El modelo 
* Los nombres de los juegos 
* Los juegos populares 

Y a la hora de recibir las recomendaciones se cargan:
* El ajuste de los datos
* La predicci贸n o transformaci贸n del modelo 
* La transformaci贸n de los datos de salida

##  7. Aplicaci贸n de Procesamiento del Lenguaje Natural: Chatbot con dialog flow 

Para el apartado del Lenguaje Natural, se ha decidido usar un Chat bot, concretamente dialog flow, a帽adido este a los datos principales de la aplicaci贸n,
acto seguido se mostrar谩 de manera visual como se funciona dicho a帽adido al proyeto.

<img width="679" alt="image" src="https://user-images.githubusercontent.com/65163077/224585308-6cd6518e-00e1-471c-9aa5-a8fc1d124287.png">

En esta imagen mostraremos lo principal sobre el mantenimiento y uso de Dialog flow de entre ellos distintas secciones:

* Intents: Es donde colocaremos las respuestas y preguntas realizadas por el bot, dandose asi a una pregunta diferentes respuestas en cuestion.

* Entities: Esta secci贸n va destinada a la hora de que una palabra o varias palabras tengan un sentido en comun, dandose asi casos de sinonimos u otras referencias, mediante las entidades podemos sacar un valor clave en la pregunta y el sistema lo detectara automaticamente dando as铆 una de tantas respuestas segun sea lo que se ha fijado.

* Integrations: Utilizada para poder aportar Dialog Flow a las distintas secciones del proyecto y sus exportaciones del mismo.

Ahora bien, iremos por parte principalmente con dos de las secciones ya mencionadas, esas son Intents y Entities:

<img width="316" alt="image" src="https://user-images.githubusercontent.com/65163077/224585881-c119009f-650a-45c8-84b1-d28ed24ed855.png">

En Intents se menciona las intenciones que tiene el chat para poder devolver una respuesta adecuada a la pregunta proporcionada, en este caso tendremos las de por defecto que viene con Dialog, pero se han a帽adido 4 nuevas, las cuales son:

* Knox - Como archivo principal de saludos del bot e inicio del mismo.

<img width="577" alt="image" src="https://user-images.githubusercontent.com/65163077/224586046-5528a091-b31e-4d7b-a926-8fcb9e5fa855.png">


* Juegos-Accion: En este archivo estan recopilados peque帽as informaciones sobre los juegos de esa misma categor铆a, a帽adiendo tambi茅n algunas respuestas.

<img width="589" alt="image" src="https://user-images.githubusercontent.com/65163077/224586075-f441a631-0951-4356-9825-fd3e0cdd7995.png">


* Juegos-Terror: En este archivo estan recopilados peque帽as informaciones sobre los juegos de esa misma categor铆a, a帽adiendo tambi茅n algunas respuestas.

<img width="594" alt="image" src="https://user-images.githubusercontent.com/65163077/224586107-4ab244e8-0cee-48d4-be8f-a86206812ab5.png">


*Juegos-Rol: En este archivo estan recopilados peque帽as informaciones sobre los juegos de esa misma categor铆a, a帽adiendo tambi茅n algunas respuestas.

<img width="563" alt="image" src="https://user-images.githubusercontent.com/65163077/224586142-d6cf689c-35e0-4daa-92ca-424d1a0c244a.png">

Ahora pasaremos a las Entities:

<img width="598" alt="image" src="https://user-images.githubusercontent.com/65163077/224586201-e828b667-bbd8-45e5-a306-d0b863fb4f06.png">

Dentro de esta tendremos una serie de recopilaci贸n de palabras clave, las cu谩les sirven para determinar a la hora de preguntar algo al Bot, que este identifique dicha palabra dentro de los dem谩s cuadros de los Intents

Dialog Flow tambi茅n aparte un peque帽o recuadro de pruebas vease como este:

<img width="171" alt="image" src="https://user-images.githubusercontent.com/65163077/224586287-e33f86eb-d71a-45cf-b8e3-399e1dd1d82b.png">

Ahora procederemos a una visual dentro del mismo proyecto:

<img width="519" alt="image" src="https://user-images.githubusercontent.com/65163077/224586339-a7ee81f2-b723-493f-afd3-731faaf6b666.png">

Dentro de la misma p谩gina accederemos al apartado del ChatBot, en este veremos el cuadro a la espera de preguntar distintas opciones:

<img width="216" alt="image" src="https://user-images.githubusercontent.com/65163077/224586396-b6296182-d8a3-4267-90a5-089e2c1cd2c5.png">

Si comenzamos con uno de los comandos que ser铆a inicio, este nos devolvera una respuesta cordial.


<img width="180" alt="image" src="https://user-images.githubusercontent.com/65163077/224586443-85bfeb32-6c9d-41ee-908b-ff3b5e5701af.png">

Si le pedimos que nos devuelva los juegos de rol mejores recomendados por Knox-Quack, este nos devolvera una peque帽a lista junto con una peque帽a recomendaci贸n que otra.

<img width="178" alt="image" src="https://user-images.githubusercontent.com/65163077/224586752-9cf8a742-11e3-45bd-b663-35a5a144be1f.png">

Lo mismo pasa con los juegos de accion y de terror en dichos casos

<img width="203" alt="image" src="https://user-images.githubusercontent.com/65163077/224587103-ca097012-aa00-4e8c-aae8-2556cf8c016f.png">



##  8. Aplicaci贸n Web: Dockerizaci贸n y despliegue

Si bien ajustar las cosas para evitar que nuestra aplicaci贸n cargara demasiadas cosas desde la base de datos ha sido 
la parte m谩s tediosa, resolver los problemas que pueden plantear las distintas versiones, la falta de disponibilidad en 
m谩quinas debian de java 8 o las versiones demasiado antiguas que ven铆an en algunas im谩genes de docker supusieron un 
d铆a entero de pruebas y errores. La decisi贸n final fue crear una imagen de docker partiendo de una imagen de ubuntu 
jammy, sistema en el que se realiz贸 y funciona esta aplicaci贸n perfectamente. Una vez que se entiend docker es sencillo. 

Aunque el Dockerfile qued贸 al final un poco sucio con tanta depuraci贸n realiza:
* Instalaci贸n de `python3` con `pip` 
* pipenv - Se iba a usar y se us贸 en una prueba para obtener un `requirements.txt` fiable de la aplicaci贸n 
* streamlit - aunque se instala con `requirements.txt`
* Java 8 
* `Spark` en su versi贸n `3.2.3`
* Definici贸n de las variables de entorno `$JAVA_HOME` y `$SPARK_HOME` 
* Lo necesario tambi茅n para instalar mongodb (Este paso es necesario para que la aplicaci贸n funcione)
* Definici贸n de variables de mongodb(tambi茅n necesario)
* Se define el entorno virtual en el proyecto 
* Se instalan los `requirements.txt`
* Se expone el puerto de `streamlit`
* Se ejecuta

![Captura desde 2023-03-12 18-20-11](https://user-images.githubusercontent.com/116188406/224563669-bd1229cb-d9b9-4f60-bc31-538ec595e1a8.png)


Para su despliegue en Streamlit Cloud fue adema艣 necesario a帽adir un archivo `packages.txt` con la especificaci贸n del paquete de java 8 si no
se hac铆a Streamlit arroja una `JavaGatewayException`. 

Por 煤ltimo solo es necesario definir la url del cluster de mongodb en el archivo de producci贸n y ponerla como est谩 con `streamlit.secrets`

##  9. Conclusiones

Este proyecto fue dise帽ado para que los usuarios utilizaran y navegasen por esta interfaz para resolver sus dudas a la hora de buscar datos sobre un juego en especifico, tambi茅n de saber si val铆a la pena adquirir dicho juego o no.

Hay muchas mejoras de por medio, tanto la visualizaci贸n como ciertos aspectos de tema IA, como lo es nuestro ChatBot integrado, sin duda ha sido un proyecto interesante y ciertamente con ganas de progresar en 茅l para ver hasta cuan lejos puede llegar esta idea con esfuerzo diario.

## Construido con 馃洜锔?

## Framework web
<img src="https://upload.wikimedia.org/wikipedia/commons/7/77/Streamlit-logo-primary-colormark-darktext.png" height="60px">

## Lenguajes de programaci贸n
<img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" height="60px">

<img src="https://camo.githubusercontent.com/b713d9f05063e22ec2ef142d1ea4f28d4a735e96f12943efb7afc6a1e30298d6/68747470733a2f2f342e62702e626c6f6773706f742e636f6d2f2d444c41614f62634e4b75512f5842596d34737873745a492f41414141414141414151772f693749784e6d45526c53415945474e4848356e582d4f2d6c6373666c5857484377434c63424741732f73313630302f6a617661382e6a7067" height="100px">

## Bases de datos y sistemas de Machine Learning y Big Data

<img src="https://www.pngitem.com/pimgs/m/90-907131_apache-spark-mllib-logo-hd-png-download.png" height="60px">

<img src="https://upload.wikimedia.org/wikipedia/commons/9/93/MongoDB_Logo.svg" height="60px">

<img src="https://upload.wikimedia.org/wikipedia/commons/e/ed/Pandas_logo.svg" height="60px">

## Despliegue 

<img src="https://logos-world.net/wp-content/uploads/2021/02/Docker-Logo.png" height="60px">


## Servicio de despliegue utilizado 馃枃锔?

_El servicio de despliegue usado para esta ocasi贸n es Streamlit, debido a su gu铆a y accesibilidad bien expuesta para el usuario de forma que se pueda subir y desplegar con mayor facilidad._

Link de la aplicaci贸n: https://aresonay-knoxquack-app-5jrn6s.streamlit.app/

Link del video de la aplicaci贸n: https://youtu.be/wbFd0VLiilk


## Autores 鉁掞笍

* Ismael Armada Gonz谩lez
* 脕ngel Ser贸n M谩rquez
