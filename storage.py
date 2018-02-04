import asyncio
import os

import peewee
import peewee_async

# Nothing special, just define model and database:

database = peewee_async.PostgresqlDatabase(
    database=os.getenv("DB"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"))

Repo = objects = peewee_async.Manager(database)


class Subscriber(peewee.Model):
    city = peewee.CharField()
    state = peewee.CharField()
    email = peewee.CharField(primary_key=True)

    class Meta:
        database = database


Subscriber.create_table(True)
database.set_allow_sync(False)
