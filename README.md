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

##  6. Integración del modelos en la aplicación 

##  7. Aplicación de Procesamiento del Lenguaje Natural: Chatbot con dialog flow 

##  8. Aplicación Web: Dockerización y despliegue

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
