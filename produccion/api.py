from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import spotipy
import math
from spotipy.oauth2 import SpotifyClientCredentials
import json

features = ['energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'instrumentalness', 'danceability', 'duration_ms', 'loudness', 'valence']
moods = ['happy', 'aggressive', 'relaxing', 'dark']

#Definiendo aplicación
app = Flask(__name__)

#Método para obtener features de canciones
def get_track_features(track_ids, spotify):
    global features

    batch_size = 25
    num_batches = int(math.ceil(len(track_ids) / float(batch_size)))
    features_add = []
    for i in range(num_batches):
        batch_track_ids = track_ids[i * batch_size:min((i + 1) * batch_size, len(track_ids))]
        batch_features = spotify.audio_features(tracks=batch_track_ids)
        features_add.extend(batch_features)

    features_df = pd.DataFrame(features_add).drop(['id', 'analysis_url', 'key', 'mode', 'time_signature',
                                                   'track_href', 'type', 'uri'], axis=1)
    features_df = features_df[features]
    return features_df

def extractFeatures(playlist):
    #Conexión a Spotify API
    client_credentials_manager = SpotifyClientCredentials(client_id='5d7ab1656719472d87e78d3869d54a84', client_secret='8c74e7a5644040d4b5b940dfb2860b85')
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    tracks = pd.DataFrame()

    #Obteniendo las canciones de la playlist
    id = playlist[34:56]
    try:
        pl_tracks = spotify.playlist_tracks(id)['items']
        ids = [foo['track']['id'] for foo in pl_tracks]
    except:
        print ('Error obtaining tracks from playlist')
        
    #Obteniendo las features requeridas de cada canción
    track_features = get_track_features(ids, spotify)
    track_features['id'] = ids
    tracks = tracks.append(track_features)

    track_names = []
    track_artists = []


    #Obteniendo nombre de canción y artista
    tracks_info = spotify.playlist(id)

    for item in tracks_info['tracks']['items']:
        track_names.append(item['track']['name'])
        track_artists.append(item['track']['artists'][0]['name'])

    tracks.insert(0,column='name', value = track_names)
    tracks.insert(1, column='artist', value = track_artists)

    return tracks

@app.route("/mood", methods = ["POST"])

def mood():
    global moods
    global features
  
    if model: 
        try:
            #Obteniendo el json de entrada
            json_ = request.json
            playlist = json_[0]["playlist"]
            mood = json_[0]["mood"]

            if not mood.lower() in moods:
                return jsonify ({"error": "Unexistent mood"})
            
            tracks = extractFeatures(playlist)
            x = tracks[features]
            
            #Escalando los datos tal y como se hizo en el modelo
            scaler = StandardScaler()
            x_scaled = scaler.fit_transform(x)

            #Efectuando predicción
            y = list(model.predict(x_scaled))

            #Definiendo resultados
            i = 0
            result = []

            for item in y: 
                if item.lower() == mood.lower():
                    result.append({"artist": tracks.iloc[i]["artist"], "song": tracks.iloc[i]["name"]})
                i += 1

            print(result)
            print(type(result))

            return jsonify (result)

        except:
            return jsonify ({"error": traceback.format_exc()})
    else:
        return jsonify ({"error": "Invalid model"})
        
if __name__ == "__main__":
    model = joblib.load("music_mood_model.pkl")
    print("Modelo cargado")
    features = joblib.load("features.pkl")
    print("Características cargadas")
    app.run(debug=True)


    