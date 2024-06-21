from flask import Flask, jsonify
import database

app = Flask(__name__)


@app.route('/api/reviews', methods=['GET'])
def api_get_reviews():
    reviews = database.get_all_reviews()
    response = []
    for item in reviews:
        response.append({
            'nickname': item[0],
            "review": item[1]
        })
    return jsonify(response)


@app.route('/api/rooms', methods=['GET'])
def api_get_rooms_with_orders():
    rooms_with_orders = database.get_rooms_with_orders()
    response = []
    for item in rooms_with_orders:
        response.append({
            'nickname': item[1],
            "roomNumber": item[0],
            "order": item[2],
            "id": item[3]
        })
    return jsonify(response)


@app.route('/api/rooms/<order_id>', methods=['POST'])
def api_delete_order(order_id):
    database.delete_order(order_id)
    return '', 204
