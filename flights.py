from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Text,BigInteger
from sqlalchemy.orm import relationship,backref
from db_config import Base


class Flight(Base):
    __tablename__ = 'flights'

    # static fields
    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger(),ForeignKey('airline_companies.id', ondelete='CASCADE'),nullable=False)
    origin_country_id=Column(BigInteger(),ForeignKey('countries.id', ondelete='CASCADE'),nullable=False)
    destination_country_id = Column(BigInteger(),ForeignKey('countries.id', ondelete='CASCADE'),nullable=False)
    departure_time = Column(DateTime)
    landing_time = Column(DateTime)
    remaining_tickets = Column(BigInteger)


    airline_company = relationship(
        "Airline_Company", backref=backref("flights", uselist=True, passive_deletes=True))
    origin_country = relationship(
        "Country", foreign_keys=[origin_country_id], uselist=True, passive_deletes=True)
    destination_country = relationship(
        "Country", foreign_keys=[destination_country_id], uselist=True, passive_deletes=True)




    def __repr__(self):
        return f'\n<Flights id={self.id} username={self.Airline_Company_Id} email={self.Origin_Country_Id} date_created={self.Destination_Country_Id}>' +\
    f'depature time = {self.Departure_Time} landing time = {self.Landing_Time} remaining_tickets = {self.Remaining_Tickets}'

    def __str__(self):
        return f'\n<Flights id={self.id} username={self.Airline_Company_Id} email={self.Origin_Country_Id} date_created={self.Destination_Country_Id}>' + \
               f'depature time = {self.Departure_Time} landing time = {self.Landing_Time} remaining_tickets = {self.Remaining_Tickets}'
