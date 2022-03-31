from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Text,BigInteger
from sqlalchemy.orm import relationship,backref
from db_config import Base


class Airline_Company(Base):
    __tablename__ = 'airline_companies'

    # static fields
    # static fields
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(),unique=True)
    country_id=Column(BigInteger(), ForeignKey('countries.id', ondelete='CASCADE'),nullable=False)
    user_id = Column(BigInteger(),ForeignKey('users.id', ondelete='CASCADE'),unique=True)

    countries = relationship('Country', backref=backref('airline_companies', uselist=True, passive_deletes=True))
    users = relationship('User', backref=backref('airline_companies', uselist=True, passive_deletes=True))



    def __repr__(self):
         return f'\n<airline_companies id={self.id} name={self.Name} country_id={self.Country_Id} user_id={self.User_Id}>'

    def __str__(self):
        return f'\n<airline_companies id={self.id} name={self.Name} country_id={self.Country_Id} user_id={self.User_Id}>'
