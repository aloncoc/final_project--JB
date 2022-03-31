from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Text,BigInteger,TEXT
from sqlalchemy.orm import relationship
from db_config import Base
from sqlalchemy.sql import text


class Country(Base):
    __tablename__ = 'countries'

    # static fields
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(),unique=True)

    def __repr__(self):
        return f'\n<countries id={self.id} name={self.name}>'

    def __str__(self):
        return f'\n<countries id={self.id} name={self.name}>'
