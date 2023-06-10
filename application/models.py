import os
import bcrypt
from flask_login import UserMixin
from mongoengine import \
    connect, \
    Document, \
    StringField, \
    ListField, \
    EmbeddedDocumentField, \
    EmbeddedDocument, \
    FloatField, \
    IntField

PASSWORD = os.getenv('MONGO_DB_PW')
DATABASE = "house_look_one"
uri = f"mongodb+srv://zacchaeus:{PASSWORD}@cluster0.54apo0d.mongodb.net/{DATABASE}?retryWrites=true&w=majority"
connect(host=uri)

class Room(EmbeddedDocument):
    room_type = StringField(required=True)
    room_price = FloatField(required=True)
    room_vacancies = IntField(required=True)
    room_images = ListField(StringField())

class House(Document):
    house_name = StringField(required=True)
    house_location = StringField(required=True)
    house_image = StringField()
    house_rooms = ListField(EmbeddedDocumentField(Room), required=False)


class User(UserMixin, Document):
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    def set_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    @staticmethod
    def get_by_email(email):
        return User.objects(email=email).first()

    def get_id(self):
        return str(self.id)



