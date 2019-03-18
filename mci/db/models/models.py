"""Database Models.

This module contains all MCI database models.

"""

from mci.app.app import db


class Thing(db.Model):
    thing = db.Column(db.String(100), primary_key=True)
