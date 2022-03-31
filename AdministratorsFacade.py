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
from Administrators import Administrator
from logger import Logger
from WrongCredentialsException import WrongCredentialsException
from DuplicateValueError import DuplicateValueError
from InvalidInput import InvalidInput
from InvalidUser_roleError import Invalid_User_role
from AirlineNotFoundError import AirlineNotFound
from UserAlreadyExistError import UserAlreadyExitsError
from UserNotExistError import UserNotExist
from CountryNotExistError import CountryNotExist
from InvalidTokenError import InvalidToken



class AdmininstratorFacade(FacadeBase):
    def __init__(self,login_token):
        super().__init__()
        self.login_token = login_token

    def get_all_customers(self,customers):
        if not isinstance(customers,Customer):
            print('must be instance of class customer')
            return
        return self.repo.get_all(customers)

    def add_admin(self,admin):
        self.logger.logger.debug(f'Attepmting  to activate add_admin function.')
        if not isinstance(admin, Administrator):
            self.logger.logger.error(F'function add_admin failed {InvalidInput}')
            raise InvalidInput('must be instance of class admin')

        if self.repo.get_by_id(Administrator,admin.id) != None:
            self.logger.logger.error(f'Function add_admin failed {DuplicateValueError}')
            raise DuplicateValueError(f'id: {admin.id} already exist')
        if self.repo.get_by_condition(Administrator,lambda query:query.filter(Administrator.user_id == admin.user_id).all()):
            self.logger.logger.error(f'Function add_admin failed {DuplicateValueError}')
            raise DuplicateValueError(f'user_id {admin.user_id} already in use')
        if self.repo.get_by_id(User,admin.user_id) == None :
            self.logger.logger.error(f'{WrongCredentialsException} Function add_admin failed')
            raise WrongCredentialsException(f'user : {admin.user_id} not exist')
        user_ = self.repo.get_by_id(User,admin.user_id)
        if user_.user_role != 1:
            self.logger.logger.error(f'{Invalid_User_role},Function add_admin failed!')
            raise Invalid_User_role(f'user {admin.user_id} is not admin!')
        self.repo.add(admin)
        self.logger.logger.info('Function new_admin has sucsessfuly activated.')
        return True

    def remove_airline(self,id):
        self.logger.logger.debug('Attepmting to activate remove_airline function.')
        if not isinstance(id,int):
            self.logger.logger.error(f'Function remove_airline failed {InvalidInput}')
            raise InvalidInput(f'id: {id} must be integer')
        airline = self.repo.get_by_id(Airline_Company,id)
        if airline == None:
            self.logger.logger.error(F'Function remove_airline failed {AirlineNotFound}')
            raise AirlineNotFound(f'airline id :{id} not exist')
        if self.login_token.role != 'Admin':
            self.logger.logger.error(F'{InvalidToken}')
            raise InvalidToken
        else:
            airline_user_id = airline.user_id
            self.repo.delete_by_id(Airline_Company,Airline_Company.id,id)
            self.logger.logger.info(f'Function remove_ariline sucsessfuly activated on airline_id :{id}')
            self.repo.delete_by_id(User,User.id,airline_user_id)
            self.logger.logger.info(f'User :{airline_user_id} deleted from db')


    def remove_customer(self,id):
        self.logger.logger.debug('Attepmting to activate Function remove_customer')
        if not isinstance(id,int):
            self.logger.logger.info(f'Function remove_customer failed {InvalidInput}')
            self.logger.logger.error(f'{InvalidInput} id must be integer')
            raise InvalidInput
        if self.login_token.role != 'Admin':
            self.logger.logger.error(F'{InvalidToken}')
            raise InvalidToken
        if self.repo.get_by_id(Customer,id) == None:
            self.logger.logger.error(f'Function remove_customer failed {WrongCredentialsException}')
            raise WrongCredentialsException(f'customer {id} not exist')
        self.repo.delete_by_id(Customer, Customer.id, id)
        self.logger.logger.info(f'Function remove_customer sucsessfuly activated on customer_id :{id}')

    def remove_administrator(self,id):
        self.logger.logger.debug('Attepmting to activate remove_administrator function')
        if not isinstance(id,int):
            self.logger.logger.error(f' Function remove_administrator failed {InvalidInput}')
            print('id must be integer')
            return
        if self.login_token.role != 'Admin':
            self.logger.logger.error(F'{InvalidToken}')
            raise InvalidToken
        if self.repo.get_by_condition(Administrator,lambda query:query.filter(Administrator.id != id)):
            self.logger.logger.error(f'Function remove_admininstrator failed {WrongCredentialsException}')
            print('admin not exist')
            return
        self.repo.delete_by_id.query(Airline_Company).filter(Administrator.id == id).all()
        self.logger.logger.info(f'Function remove_administrator sucsessfuly activated on admin_id: {id}')

    def add_customer(self, user, customer):
        self.logger.logger.debug(
            f'Attempting to used the function <<add_customer>> by administrator <<{self.login_token.id}>>')
        if not isinstance(user,User):
            self.logger.logger.error(
                f'Function <<add_customer>> failed. Admin <<{self.login_token.id}>>. Invalid class Users')
            raise InvalidInput
        elif not isinstance(customer, Customer):
            self.logger.logger.error(
                f'Function <<add_customer>> failed. Admin <<{self.login_token.id}>>. Invalid class Customers')
            raise InvalidInput
        elif self.repo.get_by_condition(
                Customer, lambda query: query.filter(Customer.phone_no == customer.phone_no).all()):
            self.logger.logger.error(
                f'Function <<add_customer>> failed. Admin <<{self.login_token.id}>>. Invalid user role')
            raise DuplicateValueError
        elif self.repo.get_by_condition(Customer, lambda query: query.filter(
                Customer.credit_card_no == customer.credit_card_no).all()):
            self.logger.logger.error(
                f'Function <<add_customer>> failed. Admin <<{self.login_token.id}>>. Invalid credit card number')
            raise WrongCredentialsException
        elif user.user_role !=2 :
            raise Invalid_User_role
        else:
            user.user_role = 2
            user.id = None
            self.create_user(user)
            customer.id = None
            self.repo.add(customer)
            print('\nAdding a new customer approved')
            self.logger.logger.info(
                f'Adding a new customer approved <<{customer.id}>>. Admin <<{self.login_token.id}>>')
            return True



    def add_airline(self,airline,user):
        self.logger.logger.debug('attepmting to activate add_arline function')
        if not isinstance(airline, Airline_Company):
            self.logger.logger.error(f'{InvalidInput} airline must be instance of class Airline_Company')
            raise InvalidInput('airline must be instance of class Airline_Company')
        if not isinstance(user, User):
            self.logger.logger.error(f'{InvalidInput} - User must be a "Users" object!')
            raise InvalidInput('Input must be a "Users" object!')
        airline_user = (User,airline.user_id)

        if self.repo.get_by_condition(Airline_Company,lambda query:query.filter(Airline_Company.id == airline.id)).all():
            self.logger.logger.error(f'{DuplicateValueError}')
            raise DuplicateValueError(f'airline_id:{airline.id} already exists')
        if self.repo.get_by_condition(Airline_Company,lambda query:query.filter(Airline_Company.name == airline.name)).all():
            self.logger.logger.error(f'Function add_airline Failed {DuplicateValueError}')
            raise DuplicateValueError(f'name :{airline.name} already exists')
        if self.repo.get_by_condition(Airline_Company,lambda query:query.filter(Airline_Company.user_id == airline.user_id)).all():
            self.logger.logger.error(f'Function add_airline Failed {DuplicateValueError}')
            raise DuplicateValueError(f'user_id {airline.user_id} already in use')
        airline_country = self.repo.get_by_id(Country,airline.country_id)
        if airline_country == None:
            self.logger.logger.error(f'{CountryNotExist}')
            raise CountryNotExist(f'Country_id {airline.country_id} not exist')
        if user.user_role !=3:
            self.logger.logger.error(f'{Invalid_User_role},Function add_airline failed!')
            raise Invalid_User_role('use_role not match!')
        else:
            user.user_role = 3
            user.id = None
            self.create_user(user)
            airline.id = None
            self.repo.add(airline)
            self.logger.logger.info(f'airline {airline.id} has added.')
            return True
