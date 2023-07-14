from flask import Flask, request, jsonify
from flask_cors import CORS

from service.fodu_service import FoduService

app = Flask(__name__)
CORS(app)

fodu_service = FoduService()


@app.route('/')
def hello_world():
    print("Hello, World!")
    return "Hello, World!"


@app.route('/query', methods=['POST'])
def process_query():
    try:
        data = request.get_json()
        if 'query' not in data:
            return jsonify({'error': 'Missing query parameter'}), 404
        query = data['query']
        print("Received query:", query)
        # Perform processing on the query and generate a result
        result = fodu_service.generate_result(query)
        return jsonify(result), 200
    except Exception as e:
        return jsonify(str(e)), 500


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
