from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the model from the pickle file
with open('RidgeModel.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    data = request.get_json()
    values = data['values']

    #input_data = np.array(values).reshape(1, -1)
    column_names = ['location','total_sqft','bath','bhk']

    input_data = pd.DataFrame([values], columns=column_names)

    # Make prediction
    prediction = model.predict(input_data)
    
    # Return prediction as JSON
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
