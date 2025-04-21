
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Simulaciones en memoria
db = {
    'alumnos': [],
    'docentes': [],
    'materias': [],
    'preceptores': []
}
id_counter = {k: 1 for k in db}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<tipo>', methods=['GET', 'POST'])
def gestionar_lista(tipo):
    if request.method == 'POST':
        data = request.get_json()
        data['id'] = id_counter[tipo]
        db[tipo].append(data)
        id_counter[tipo] += 1
        return jsonify({'ok': True}), 201
    return jsonify(db[tipo])

@app.route('/<tipo>/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def gestionar_item(tipo, item_id):
    items = db[tipo]
    item = next((i for i in items if i['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'No encontrado'}), 404
    if request.method == 'GET':
        return jsonify(item)
    elif request.method == 'PUT':
        data = request.get_json()
        for k in data:
            item[k] = data[k]
        return jsonify({'ok': True})
    elif request.method == 'DELETE':
        db[tipo].remove(item)
        return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(debug=True)
