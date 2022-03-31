from abc import ABC, abstractmethod
from datetime import datetime
from Flights import Flight
from DbRepo import DbRepo
from db_config import local_session
from Airline_Companies import Airline_Company
from Country import Country
from Customers import Customer
from Users import User
from logger import Logger
from WrongCredentialsException import WrongCredentialsException
from PasswordTooShort import PasswordTooShortError
from InvalidInput import InvalidInput
from DuplicateValueError import DuplicateValueError
from InvalidUser_roleError import Invalid_User_role



class FacadeBase(ABC):
    @abstractmethod
    def __init__(self):
        self.repo = DbRepo(local_session)
        self.logger = Logger.get_instance()


    def get_all_flights(self):
        return self.repo.get_all(Flight)

    def get_flight_by_id(self,id):
        if not isinstance(id,int):
            raise InvalidInput('id must be integer.')
        if id <=0 :
            raise InvalidInput('id must be positive')
        else:
            return self.repo.get_by_id(Flight, id)
    

    def get_flights_by_parameter(self,origin_country_id,destination_country_id,date):
        return self.repo.get_by_condition(Flight,lambda query : query.filter(Flight.origin_country_id == origin_country_id,
                                                                              Flight.destination_country_id == destination_country_id,
                                                                              Flight.departure_time == date).all())
  
    def get_all_airlines(self):
        return self.repo.get_all(Airline_Company)

    def get_all_airlines_by_id(self,id):
        return self.repo.get_by_condition(Airline_Company,lambda query : query.filter(Airline_Company.id == id).all())


    def create_user(self,user):
        if not isinstance(user,User):
            self.logger.logger.error(
                f'{InvalidInput},not instance - of class user')
            raise InvalidInput('must be instance of class user')
        if self.repo.get_by_condition(User,lambda query : query.filter(User.username == user.username).all()):
            self.logger.logger.error(f'{DuplicateValueError} username already exists')
            raise WrongCredentialsException('input invalid')
        elif self.repo.get_by_condition(User,lambda query : query.filter(User.email == user.email).all()):
            self.logger.logger.error(f'{DuplicateValueError}-email already exists in db ')
            raise DuplicateValueError('cannot create more than 1 account with the same email')
        elif len(user.password) <= 6:
            self.logger.logger.error(f'{PasswordTooShortError} password has less than 6 chars')
            raise PasswordTooShortError('password must contain at least 6 chars')
        if user.user_role not in {1,2,3}:
            self.logger.logger.error(f'{Invalid_User_role}')
            raise Invalid_User_role(f'user_role {user.user_role} not exist')
        else:
            user.id = None
            self.repo.add(user)
            self.logger.logger.info('function create_user sucssed a new user added to db')
            print(f' new user created welcome {user.username}')
            return True



