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
        json_object = Brevet.objects().to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        input_json = request.get_json()
        start_time = input_json["start_time"]
        brevet_dist = input_json["brevet_dist"]
        controls = input_json["controls"]

        Brevet(start_time=start_time, brevet_dist=brevet_dist, controls=controls).save()

        return {'_id': ""}, 200
