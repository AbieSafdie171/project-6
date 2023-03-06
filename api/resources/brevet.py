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
        json_object = Brevet.objects.get(id=_id).to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def put(self, _id):
        brevet = Brevet.objects.get(id=_id).to_json()

        brevet.update(start_time = brevet["start_time"],
                      brevet_dist = brevet["brevet_dist"],
                      controls = brevet["controls"])

        return {'id': str(_id), 'status': 'updated'}, 200

    def delete(self, _id):
        Brevet.objects.get(id=_id).delete()
        return {'_id': str(_id)}, 200
