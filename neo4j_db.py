# neo4j_db.py
from neo4j import GraphDatabase
import logging
import json

# Configure the logger
logging.basicConfig(level=logging.DEBUG,  # Set the logging level
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Create a logger object
logger = logging.getLogger('my_logger')

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def update_or_create_prediction(self,data):
        logger.info("whats the value  11111>>>",data)
        with self.driver.session() as session:
            result = session.write_transaction(self._update_or_create_prediction,data)
            return result
                
    @staticmethod
    def _update_or_create_prediction(tx,data):
        logger.info("whats the value 33333 >>>",data)
     
        # Step 3: Parse the JSON string to a Python dictionary
        data = json.loads(data)

        # Step 4: Extract the value from the dictionary
        # Assuming the value is within a list under the 'prediction' key
        prediction = data['prediction'][0]
        
        logger.info("whats the value 4444 >>>",prediction)

        query = (
            "MERGE (p:PredictionAPI {prediction: $prediction}) "
            "ON CREATE SET p.prediction = $prediction "
            "ON MATCH SET p.prediction = $prediction "
            "RETURN p"
        )
        result = tx.run(query, prediction=prediction)
        record = result.single()
        if record:
            node = record["p"]
            return {
                "id": node.id,
                "labels": list(node.labels),
                "properties": dict(node.items())
            }
        else:
            return None
