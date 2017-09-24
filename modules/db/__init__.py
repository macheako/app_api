import peewee
from peewee import *

db = MySQLDatabase()

class BaseModel(Model):
    class Meta:
        database = db