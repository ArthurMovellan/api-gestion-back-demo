from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from src.database import db_dao
from src.services import db_service
import json
# import src.env
import logging

app = Flask(__name__)
db = db_dao.Database()

logging.basicConfig(level=logging.INFO)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['POST','GET'])
def index():
    """ Used function in order to avoid 404 return on POST or GET methods on the root
    Returns:
        JSON that contains "'API': 'EMAC'" and returned code 200
    """
    return make_response(jsonify({'API': 'EMAC'}), 200)

@app.errorhandler(404)
def not_found(error):
    """ Used function in order to return 404 code when non-existing route
    Args:
        error : catched error when using non-existing route
    Returns:
        JSON that contains "Resource not found" message and returned code 404
    """
    return make_response(jsonify({'error': f'Resource not found: "{error}"'}), 404)

@app.errorhandler(405)
def method_not_allowed(error):
    """ Used function in order to return 405 code when not allowed method on concerned route
    Args:
        error : catched error when using not allowed method
    Returns:
        JSON that contains "Bad request method" message and returned code 405
    """
    return make_response(jsonify({'error': f'Bad request method: "{error}"'}), 405)

@app.route('/customers', methods=['GET'])
def get_customer():
    logging.info("Received a GET request on route : customers")
    
    try:
        customers = db_service.get_customers_db(db)
    except Exception as ex:
        logging.error(str(ex))
        return make_response(jsonify({"message": str(ex)}), 500)

    return make_response(jsonify(customers), 200)

@app.route('/items', methods=['POST'])
def get_items():
    logging.info("Received a POST request on route : items")
    
    try:
        data = request.form.get("data")
        data_json = json.loads(data)
        customer_id = data_json['customer']
        items = db_service.get_items_by_customer_id_db(db, customer_id)
    except Exception as ex:
        logging.error(str(ex))
        return make_response(jsonify({"message": str(ex)}), 500)

    return make_response(jsonify(items), 200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)