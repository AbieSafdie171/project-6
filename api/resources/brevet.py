"""
Resource: Brevet
"""
from flask import Response, request
from flask_restful import Resource
from datetime import datetime

# You need to implement this in database/models.py
from database.models import Brevet, Control


class BrevetApi(Resource):
    def get(self, _id):
        # Get the brevet from the id
        json_object = Brevet.objects.get(id=_id).to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def put(self, _id):
        # Update a brevet from the database
        input_json = request.json

        Brevet.objects.get(id=_id).update(**input_json)

        return '', 200

    def delete(self, _id):
        # Delete brevet from database
        Brevet.objects.get(id=_id).delete()
        return '', 200

