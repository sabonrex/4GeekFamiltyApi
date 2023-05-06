"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# turn errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members

    return jsonify(response_body), 200

@app.route(('/member/<int:id>'), methods=['GET'])
def get_single_id(id):

    member = jackson_family.get_member(id)
    response_body = member
    return jsonify(response_body), 200


@app.route('/member', methods=['POST'])
def add_member():
    data = request.json
    new_member = {
        "id": data["id"],
        "first_name": data["first_name"],
        "age": data["age"],
        "lucky_numbers": data["lucky_numbers"]
    }
    jackson_family._members.append(new_member)


    return jsonify(jackson_family._members)


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    # delete section
    result = jackson_family.delete_member(id)
    
    # to delete
    if result:
        response_body = {
            "message": f"El miembro con ID {id} ha sido eliminado de la familia Jackson.",
            "done" : True
        }
        return jsonify(response_body), 200
    
    # if not found
    else:
      return jsonify(f"No se encontró ningún miembro con ID {id}.", status_code=404)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)