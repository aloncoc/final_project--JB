from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text,BigInteger
from sqlalchemy.orm import relationship,backref
from db_config import Base


class Administrator(Base):
    __tablename__ = 'administrators'

    # static fields
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(Text)
    last_name = Column(Text)
    user_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)

    users = relationship('User', backref=backref('administrators', uselist=True, passive_deletes=True))



    def __repr__(self):
        return f'\n<adminstaros id={self.id} first_name={self.First_Name} last_name={self.Last_Name} user_id={self.User_Id}>'

    def __str__(self):
        return f'\n<adminstaros id={self.id} first_name={self.First_Name} last_name={self.Last_Name} user_id={self.User_Id}>'
