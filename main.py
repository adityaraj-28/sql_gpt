import json

from flask import Flask, request, jsonify

from service.fodu_service import FoduService

app = Flask(__name__)

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


@app.route('/summary', methods=['GET'])
def gen_summary():
    try:
        lst = fodu_service.generate_summary(request.args.get('user_name'), request.args.get('org_name'))
        if len(lst) == 0:
            return jsonify({"a1": "invalid username or organization name", "a2": "invalid username or organization name", "a3": "invalid username or organization name", "a4": "invalid username or organization name"}), 200
        dct = {
            "a1": lst[0], "a2": lst[1], "a3": lst[2], "a4": lst[3]
        }
        return jsonify(dct), 200
    except Exception as e:
        return jsonify(str(e)), 500


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
