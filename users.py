from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Text,BigInteger
from sqlalchemy.orm import relationship,backref
from db_config import Base


class User(Base):
    __tablename__ = 'users'

    # static fields
    id = Column(BigInteger(), primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    password = Column(Text,nullable=False)
    email = Column(Text(),unique=False)
    user_role = Column(BigInteger(),ForeignKey('user_roles.id', ondelete='CASCADE'), nullable=False)

    role = relationship('User_Role', backref=backref('users', uselist=True, passive_deletes=True))



    def __repr__(self):
        return f'\n<Users id={self.id} username={self.username} password={self.Password} email={self.Email} use_role ={self.User_Role}>'

    def __str__(self):
        return f'\n<Users id={self.id} username={self.username} password={self.Password} email={self.Email} use_role ={self.User_Role}>'
