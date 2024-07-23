# app.py
from flask import Flask, request, jsonify
from neo4j_db import Neo4jConnection
import pickle
import numpy as np
import pandas as pd
import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Create a logger object
logger = logging.getLogger('my_logger')

app = Flask(__name__)

# Initialize the Neo4j connection
db = Neo4jConnection(uri="", user="", password="")

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
    prediction = jsonify({'prediction': prediction.tolist()})
    
    logger.info("This is an info message >>> ", prediction.get_data())

    
    # prediction = {
    #     "prediction": prediction.data
    # }

    logger.info("This is an info message 222222 >>> ", prediction.get_data())

    try:
        result = db.update_or_create_prediction(prediction.get_data())
        if result is not None:
            return jsonify({"message": "Prediction saved", "prediction": result}), 201
        else:
            return jsonify({"error": "Failed to save prediction"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"}), 200

if __name__ == '__main__':
    app.run(debug=True)
