from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """Return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    # Use the 'data' loaded from 'pictures.json'
    return jsonify(data)

######################################################################
# GET A PICTURE BY ID
######################################################################
@app.route('/picture/<int:id>', methods=['GET'])
def get_picture_by_id(id):
    # Search for the picture with the given id in 'data'
    picture = next((item for item in data if item['id'] == id), None)
    
    if picture:
        return jsonify(picture), 200
    else:
        return jsonify({'error': 'Picture not found'}), 404    

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        # Extract the picture data from the incoming request
        new_picture = request.get_json()

        # Check if the 'id' already exists in the data
        if any(picture['id'] == new_picture['id'] for picture in data):
            return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

        # Append the new picture to the data
        data.append(new_picture)

        # Return the newly created picture with a 201 status code
        return jsonify(new_picture), 201
    except Exception as e:
        # Handle any errors gracefully
        return jsonify({"error": str(e)}), 500


######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract data from the incoming request
    updated_picture = request.get_json()

    # Find the picture in the 'data' list by ID
    picture = next((item for item in data if item['id'] == id), None)

    # If the picture is found, update it
    if picture:
        picture.update(updated_picture)
        return jsonify(picture), 200
    else:
        # If the picture is not found, return a 404 error with a message
        return jsonify({"message": "picture not found"}), 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    # Find the picture with the given ID
    picture = next((item for item in data if item['id'] == id), None)

    if picture:
        # Remove the picture from the list
        data.remove(picture)
        # Return 204 No Content since no body is needed in the response
        return '', 204  # Empty body with a 204 status code
    else:
        return jsonify({"message": "picture not found"}), 404


