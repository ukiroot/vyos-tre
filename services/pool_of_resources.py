from flask import Flask, jsonify, abort, make_response, request


app = Flask(__name__)


#  pool = {
#      'eut':
#      [
#          {
#              'id': 1,
#              'name': 'EUT_1',
#              'settings': ['telnet 127.0.0.1 7001'],
#              'available': True
#          }
#      ],
#      'bridge':
#      [
#          {
#              'id': 1,
#              'name': 'mighty_bridge_1',
#              'settings': ['192.168.77.0 255.255.255.0'],
#              'available': True
#          }
#      ],
#      'linuxchan':
#      [
#          {
#              'id': 1,
#              'name': 'ursa_major',
#              'settings': [telnet 127.0.0.1 7701],
#              'available': True
#          }
#      ],
#  }


pool = {
    'eut': [],
    'bridge': [],
    'linuxchan': []
}
key_n = 'name'
key_s = 'settings'
key_a = 'available'
tr_key_s = 'status'
tr_key_w = 'who'
transaction = {
    tr_key_s: 'available',
    tr_key_w: 'some_bad_guy'
}


@app.route('/restapi/v1.0/transaction', methods=['GET'])
def get_transaction():
    return jsonify(transaction)


@app.route('/restapi/v1.0/transaction', methods=['PUT'])
def update_transaction():
    if 'who' in request.json:
        transaction[tr_key_w] = request.json[tr_key_w]
    transaction[tr_key_s] = request.json[tr_key_s]
    return jsonify(transaction)


@app.route('/restapi/v1.0/pool/<resource>', methods=['GET'])
def get_items(resource):
    return jsonify({resource: pool[resource]})


@app.route('/restapi/v1.0/pool/<resource>/<int:eut_id>', methods=['GET'])
def get_item(resource, eut_id):
    eut = [item for item in pool[resource] if item['id'] == eut_id]
    if len(eut) == 0:
        abort(404)
    return jsonify({resource: eut})


@app.route('/restapi/v1.0/pool/<resource>', methods=['POST'])
def create_item(resource):
    if not request.json or not ('name' or 'settings') in request.json:
        abort(400)
    # Todo: check that name is uniq
    if len(pool[resource]) == 0:
        new_id = 1
    else:
        new_id = pool[resource][-1]['id'] + 1
    eut = {
        'id': new_id,
        'name': request.json['name'],
        'settings': request.json['settings'],
        'available': True
    }
    pool[resource].append(eut)
    return jsonify({resource: eut}), 201


@app.route('/restapi/v1.0/pool/<resource>/<int:eut_id>', methods=['PUT'])
def update_item(resource, eut_id):
    instance = [item for item in pool[resource] if item['id'] == eut_id]
    if len(instance) == 0:
        abort(404)
    id = instance[0]['id'] - 1
    pool[resource][id][key_a] = request.json.get(key_n, instance[0][key_n])
    pool[resource][id][key_s] = request.json.get(key_s, instance[0][key_s])
    pool[resource][id][key_a] = request.json.get(key_a, instance[0][key_a])
    return jsonify({resource: pool[resource][id]})


@app.route('/restapi/v1.0/pool/<resource>/<int:eut_id>', methods=['DELETE'])
def delete_item(resource, eut_id):
    instance = [item for item in pool[resource] if item['id'] == eut_id]
    if len(instance) == 0:
        abort(404)
    id = instance[0]['id'] - 1
    pool[resource].remove(pool[resource][id])
    print(pool[resource][id])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=False)
