from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Text,BigInteger
from sqlalchemy.orm import relationship
from db_config import Base


class User_Role(Base):
    __tablename__ = 'user_roles'

    # static fields
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(),unique=True)

    
    def __repr__(self):
        return f'\n<User_roles id={self.id} role_name={self.name}>'

    def __str__(self):
        return f'\n<User_roles id={self.id} role_name={self.name}>'
