"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource
import logging
# You need to implement this in database/models.py
from database.models import Brevet, Control


class BrevetsApi(Resource):
    def get(self):
        # get the brevet
        json_object = Brevet.objects().to_json()  # converts to json
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        # Put into database and return the id
        input_json = request.json

        result = Brevet(**input_json).save()

        return {'_id': str(result.id)}, 200
