from mongoengine import *
import datetime


class Control(EmbeddedDocument):
    """
    A MongoEngine EmbeddedDocument containing:
        distance: MongoEngine float field, required, (control distance in kilometers),
		location: MongoEngine string field, optional, (control location name),
		open_time: MongoEngine string field, required, (control opening time),
		close_time: MongoEngine string field, required, (control closing time).
    """
    miles = FloatField(required=False)
    km = FloatField(required=True)
    open = StringField(required=True)
    close = StringField(required=True)
    location = StringField(required=False)


class Brevet(Document):
    """
    A MongoEngine document containing:
		brevet_dist: MongoEngine float field, required
		start_time: MongoEngine string field, required
		controls: MongoEngine list field of controls, required
    """
    brevet_dist = FloatField(required=True)
    start_time = StringField(required=True)
    controls = EmbeddedDocumentListField(Control, required=True)

