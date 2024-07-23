# neo4j_db.py
from neo4j import GraphDatabase
import logging

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

    def save_prediction(self, prediction):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_and_return_prediction, prediction)
            return result

    @staticmethod
    def _create_and_return_prediction(tx, data):
        query = (
            "CREATE (p:Prediction {prediction: $prediction}) "
            "RETURN p"
        )
        logger.info(">>>>> 111" , data["prediction"][0])
        
        result = tx.run(query,prediction=data["prediction"][0])
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
