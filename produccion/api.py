from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

@app.route("/predict", methods = ["POST"])

#def hello():
#    return "Welcome to music mood predictor!"

def predict():
    if model: 
        try:
            #Obteniendo el json de entrada
            json_ = request.json
            print(json_)

            #Convirtiendo el json en un DataFrame
            query = pd.get_dummies(pd.DataFrame(json_))
            query = query.reindex(columns=features, fill_value=0)
            
            #Escalando los datos tal y como se hizo en el modelo
            scaler = StandardScaler()
            query_scaled = scaler.fit_transform(query)

            #Efectuando predicción
            prediction = list(model.predict(query_scaled))

            return jsonify ({"mood": str(prediction) })
        except:
            return jsonify ({"trace": traceback.format_exc()})
    else:
        print("Modelo inválido")
        return("Modelo inválido")
        
if __name__ == "__main__":
    model = joblib.load("music_mood_model.pkl")
    print("Modelo cargado")
    features = joblib.load("features.pkl")
    print("Características cargadas")
    app.run(debug=True)