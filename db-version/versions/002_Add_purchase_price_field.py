from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    beer = Table('beer', meta, autoload=True)
    new_col = Column('purchase_price', Integer)
    new_col.create(beer)

def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    beer = Table('beer', meta, autoload=True)
    beer.c.purchase_price.drop()
