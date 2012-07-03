from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    beer = Table('beer', meta, autoload=True)
    new_col = Column('name_accusative', String(120))
    new_col.create(beer)

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    beer = Table('beer', meta, autoload=True)
    beer.c.name_accusative.drop()
