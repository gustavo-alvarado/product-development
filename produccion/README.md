# Clasificación del *mood* de canciones con Spotify

### Descripción

Servicio REST API para la clasificación del *mood* de las canciones de una *playlist* de Spotify. El servicio recibe como entrada la URL de la *playlist*, y el *mood* que se requiere: 

``` json
[
    {
        "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX1rVvRgjX59F?si=e914bb6c272e43f6", 
        "mood": "relaxing"
    }
]
```

Con los valores de entrada, el servicio se conecta a Spotify para extraer la información requerida del listado de canciones de la *playlist*, incluyendo el nombre de la canción, y las características requeridas para el modelo de clasificación (*energy*, *liveness*, *tempo*, *speechiness*, *acousticness*, *instrumentalness*, *danceability*, *duration_ms*, *loudness*, *valence*). El modelo de redes neuronales efectúa la predicción del *mood* de todas las canciones de la *playlist*, y finalmente, el servicio retorna el listado de canciones clasificadas con el *mood* seleccionado: 

``` json
[
    {
        "artist": "Metallica",
        "song": "Nothing Else Matters (Remastered)"
    },
    {
        "artist": "4 Non Blondes",
        "song": "What's Up?"
    },
    {
        "artist": "The Smashing Pumpkins",
        "song": "Bullet With Butterfly Wings - Remastered 2012"
    }
 ]
 ```

Se incluyen los siguientes archivos: 

* **api.py**: Servicio API utilizando Flask para publicar el modelo entrenado en un ambiente de producción. 
* **music_mood_model.pkl**: Modelo entrenado con redes neuronales para la clasificación del *mood* de una canción con una efectividad de 72%.
* **features.pkl**: Objeto con el nombre de las características de una canción (extraídas de Spotify) a utilizar para la predicción. 
* **Modelo_PD_Gustavo_Alvarado.ipynb**: Entrenamiento del modelo utilizando redes neuronales. 

### Prueba en Postman

![alt text](https://github.com/gustavo-alvarado/product-development/blob/main/produccion/Prueba%20en%20Postman.png?raw=true)


### Recomendaciones

* Ampliar el conjunto de datos de *playlists* de canciones por *mood* para mejorar la efectividad del modelo. 
* Ampliar el conjunto de datos a otros *moods* que puedan aplicarse. 

### Referencias

* https://medium.com/codex/music-mood-classification-using-neural-networks-and-spotifys-web-api-d73b391044a4
