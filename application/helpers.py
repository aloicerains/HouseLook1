# from mongoengine import Document, StringField
# import bcrypt
#
# class User(Document):
#     username = StringField(required=True, unique=True)
#     password = StringField(required=True)
#
#     def set_password(self, password):
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#         self.password = hashed_password.decode('utf-8')
#
#     def check_password(self, password):
#         return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))