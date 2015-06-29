#!/usr/bin/env python3

import os

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

# Eve imports
from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL

# Eve-SQLAlchemy imports
from eve_sqlalchemy.decorators import registerSchema

Base = declarative_base()


class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime,  default=func.now())
    _updated = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now())
    _etag = Column(String)
    _id = Column(Integer, primary_key=True, autoincrement=True)


@registerSchema('submission')
class Submission(CommonColumns):
    __tablename__ = 'submission'
    url = Column(String(2000))
    author = Column(String(200))
    author_url = Column(String(2000))
    author_icon = Column(String(2000))
    comment = Column(String(5000))

pg_url = 'postgresql:///?host=/tmp/pg_db&dbname=template1'
if 'OPENSHIFT_POSTGRESQL_DB_HOST' in os.environ:
    pg_url = 'postgresql://%s:%s/%s' % (
        os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
        os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
        os.environ['OPENSHIFT_APP_NAME'])

SETTINGS = {
    'SQLALCHEMY_DATABASE_URI': pg_url,
    'RESOURCE_METHODS': ['POST', 'GET'],
    'ITEM_METHODS': ['GET'],
    'DOMAIN': {
        'submission': Submission._eve_schema['submission'],
        },
}

application = Eve(auth=None, settings=SETTINGS, data=SQL)

# bind SQLAlchemy
db = application.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()

if __name__ == "__main__":
    application.run(debug=True)

