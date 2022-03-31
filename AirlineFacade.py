from abc import ABC, abstractmethod
from datetime import datetime
from User_Roles import User_Role
from Tickets import Ticket
from Flights import Flight
from DbRepo import DbRepo
from db_config import local_session
from Airline_Companies import Airline_Company
from Country import Country
from Customers import Customer
from Users import User
from FacadeBase import FacadeBase
from logger import Logger
from AirlineNotFoundError import AirlineNotFound
from WrongCredentialsException import WrongCredentialsException
from DuplicateValueError import DuplicateValueError
from InvalidInput import InvalidInput
from CountryNotExistError import CountryNotExist
from UserNotExistError import UserNotExist
from InvalidUser_roleError import Invalid_User_role
from FlightNotExistError import FlightNotExist
from DepartureTimeError import DepartureTimeError
from InvalidTokenError import InvalidToken




class AirlineFacade(FacadeBase):
    def __init__(self,login_token):
        super().__init__()
        self.login_token = login_token


        
    def get_flights_by_airline(self,airline_id):
        return self.repo.get_by_condition(Flight,lambda query:query.filter(Flight.airline_company_id == airline_id).all())

    def update_airline(self,airline,airline_id):
        self.logger.logger.debug('attepmting to activate update_airline function')
        if not isinstance(airline_id,int):
            self.logger.logger.error(f'only integer allowed {InvalidInput}')
            raise InvalidInput('airline_id must be integer')
        if not isinstance(airline,dict):
            self.logger.logger.error(f'{InvalidInput} Input must be a dictionary')
            raise InvalidInput('airline must be dictionary')
        airline_ = self.repo.get_by_id(Airline_Company,airline_id)
        if airline_ == None:
            self.logger.logger.error(f'{AirlineNotFound}  airline with id number:{airline_id} not exist')
            raise AirlineNotFound(f'airline {airline_id} not exist')
        else:
            airline_check = self.repo.get_by_id(Airline_Company, airline_id)
            if self.login_token.id != airline_check.id:
                self.logger.logger.error(f'{InvalidToken} - you cannot edit for other airline!')
                raise InvalidToken
        self.repo.update_by_id(Airline_Company,Airline_Company.id,airline_id,airline)
        self.logger.logger.info(f'Function update_airline Activated in airline_company_id :{airline_id}')


 

    def get_all_countires(self):
        return self.repo.get_all(Country).all()

    def get_country_by_id(self, id):
        return self.repo.get_by_condition(Country,lambda query : query.filter(Country.id == id).all())



    def update_flight(self,flight,flight_id):
        self.logger.logger.debug('Attepmting to activated update_flight function')
        if not isinstance(flight,dict):
            self.logger.logger.error(f'Function update_flight Failed {InvalidInput}')
            raise InvalidInput('flight must be dictionary')
        if not isinstance(flight_id, int):
            self.logger.logger.error(f'Function update_flight Failed {InvalidInput}')
            raise InvalidInput('flight_id must be integer')
        flight_object = self.repo.get_by_id(Flight,flight_id)
        if flight_object == None:
            self.logger.logger.error(f'Function update_flight Failed {FlightNotExist}')
            raise FlightNotExist(f'flight {flight_id} not exist')
        else:
            current_tickets = self.repo.get_by_id(Flight, flight_id).remaining_tickets
            self.repo.update_by_id(Flight, Flight.id, flight_id, flight)
            updated_tickets = self.repo.get_by_id(Flight, flight_id).remaining_tickets

            if updated_tickets < 0:
                self.repo.update_by_id(Flight, Flight.id, flight_id, {'remaining_tickets': current_tickets})
                self.logger.logger.error(f'{InvalidInput} - Negative number of seats is impossible!')
                raise InvalidInput
            else:
                flight_check = self.repo.get_by_id(Flight, flight_id)
                airline_check = self.repo.get_by_id(Airline_Company, flight_check.airline_company_id)
                if self.login_token.id != airline_check.id:
                    self.logger.logger.error(f'{InvalidToken} - you cannot edit for other airline!')
                    raise InvalidToken
                else:
                    self.logger.logger.info(f'Flight updated!')
                    print(f'{updated_tickets} remaining ticket(s) on flight #{flight_id}')


    def add_flight(self,flight):
        self.logger.logger.debug('Attempting to activate add_flight function')
        if not isinstance(flight,Flight):
            self.logger.logger.error(f'Function add_flight Failed {InvalidInput}')
            raise InvalidInput('flight must be instance of class Flight')
        if self.repo.get_by_condition(Flight,lambda query:query.filter(Flight.id == flight.id)).all():
            self.logger.logger.error(f'Function add_flight Failed {DuplicateValueError}')
            raise DuplicateValueError(f'flight with id:{flight.id} already exists.')
        # if self.repo.get_by_condition(Flight,lambda query:query.filter(Flight.airline_company_id != flight.airline_company_id)).all():
        if self.repo.get_by_id(Airline_Company,flight.airline_company_id) == None:
            self.logger.logger.error(f'{AirlineNotFound} Function add_flight failed')
            raise AirlineNotFound(f'airline_company_id: {flight.airline_company_id} not exists')
        if self.repo.get_by_id(Country,flight.origin_country_id) == None:
            self.logger.logger.error(f'{CountryNotExist} function add_ticket failed')
            raise CountryNotExist(f'country with id: {flight.origin_country_id} not exists.')
        if self.repo.get_by_id(Country,flight.destination_country_id) == None:
            self.logger.logger.error(f'{CountryNotExist} function add_ticket failed')
            raise CountryNotExist(f'country with id: {flight.destination_country_id} not exists.')
        if flight.departure_time >= flight.landing_time :
            self.logger.logger.error(f'Function add_flight Failed {InvalidInput}')
            raise InvalidInput('landing time cant be earlier than depature time')
        if flight.remaining_tickets < 0 :
            self.logger.logger.error(f'Function add_flight Failed {InvalidInput}')
            raise InvalidInput('remaining seats cannot be negative!')
        if flight.destination_country_id == flight.origin_country_id :
            self.logger.logger.error(f'Function add_flight Failed, {InvalidInput}')
            raise InvalidInput()
        else:
            airline_check = self.repo.get_by_id(Airline_Company, flight.airline_company_id)
            if self.login_token.id != airline_check.id:
                self.logger.logger.error(f'{InvalidToken} - you cannot edit for other airline!')
                raise InvalidToken
            self.repo.add(flight)
            self.logger.logger.info('Function add_flight has sucsussfuly activated.')

    def remove_flight(self,flight_id):
        self.logger.logger.debug('Attempting to activate remove_flight function')
        if not isinstance(flight_id,int):
            self.logger.logger.error(f'Function remove_flight failed {InvalidInput}')
            raise InvalidInput('flight_id must be integer.')
        if self.repo.get_by_id(Flight,flight_id) == None:
            self.logger.logger.error(f'Function remove_flight failed {InvalidInput}')
            raise InvalidInput(f'flight_id: {flight_id} not exists in db.')
        else:
            airline_check = self.repo.get_by_id(Airline_Company,flight_id)
            if self.login_token.id != airline_check.id:
                self.logger.logger.error(f'Function remove_flight failed {InvalidToken}')
                raise InvalidToken
            else:
                self.repo.delete_by_id(Flight,Flight.id,flight_id)
                self.logger.logger.info(f'Flight {flight_id} has been removed.')
                return True
