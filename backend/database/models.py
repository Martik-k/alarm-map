from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db)

class Alarm(db.Model):
    __tablename__ = 'alarms'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    finish = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<Alarm {self.location} - {self.start}>'

class Shelling(db.Model):
    __tablename__ = 'shellings'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    location = db.Column(db.String(50))

    def __repr__(self):
        return f'<Shelling {self.location} - {self.time}>'
