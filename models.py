from . import db

class Temperature(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    location = db.Column(db.String(30))
    fromDate = db.Column(db.String(15))
    toDate = db.Column(db.String(15))
    temperature = db.Column(db.Float)
