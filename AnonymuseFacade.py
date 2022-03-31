from abc import ABC, abstractmethod
from datetime import datetime
from logger import Logger
from Flights import Flight
from DbRepo import DbRepo
from db_config import local_session
from Airline_Companies import Airline_Company
from Country import Country
from Customers import Customer
from Users import User
from FacadeBase import FacadeBase
# from UserAlreadyExistError import UserAlreadyExitsError
from PasswordTooShort import PasswordTooShortError
from CustomerFacade import CustomerFacade
from WrongCredentialsException import WrongCredentialsException
from InvalidInput import InvalidInput
from DuplicateValueError import DuplicateValueError
from InvalidUser_roleError import Invalid_User_role
from AdministratorFacade import AdmininstratorFacade
from AirlineFacade import AirlineFacade
from LoginToken import LoginToken





class AnonymousFacade(FacadeBase):
    def __init__(self):
        super().__init__()




    def login(self,username,password):
        if not isinstance(username,str):
            self.logger.logger.error(f'Function login Failed, {InvalidInput}')
            raise InvalidInput('username must be string')
            # self.logger.logger.error(f'{WrongCredentialsException} - invalid input! must enter string')
            # raise WrongCredentialsException('username must be string')
        if not isinstance(password,str):
            self.logger.logger.error(f'Function login Failed, {InvalidInput}')
            raise InvalidInput('password must be string')


        user = self.repo.get_by_condition(User,lambda query :query.filter(User.username == username).all())
        if not user :
            self.logger.logger.error(f'{WrongCredentialsException} -{username} not exist ')
            raise WrongCredentialsException()



        if user[0].password != password:
            self.logger.logger.error(f'{WrongCredentialsException} -{password} not exist ')
            raise WrongCredentialsException()
        else:
           if  user[0].user_role == 1:
               admin_facade = AdmininstratorFacade(login_token=LoginToken(id=user[0].administrators[0].id,
                                           name=user[0].username,
                                           role='Admin'))
               self.logger.logger.info(f'welcome Admin {user[0].username}')
               return admin_facade
           elif user[0].user_role == 2:
                customer_facade = CustomerFacade(login_token=LoginToken(id=user[0].customers[0].id,
                                           name=user[0].username,
                                           role='Customer'))
                self.logger.logger.info(f'Login allowed. Customer: {user[0].username}')
                return customer_facade
           elif user[0].user_role == 3:
               airline_facade = AirlineFacade(
                   login_token=LoginToken(id=user[0].airline_companies[0].id,
                                          name=user[0].username,
                                          role='Airline'))
               self.logger.logger.info(f'Login allowed. Airline: {user[0].username}')
               return airline_facade

    def add_customer(self,user, customer):
        self.logger.logger.debug('Attepmting to activate add_customer function')
        if not isinstance(customer, Customer):
            self.logger.logger.error(F'Function add_customer failed {InvalidInput}')
            print('Function failed, customer must be an instance of the class customer.')
            raise InvalidInput('not instance of class customer')
        if not isinstance(user,User):
            self.logger.logger.error(f'Function failed {InvalidInput}')
            raise InvalidInput('not instance of class User')
        if user.user_role !=2 :
            self.logger.logger.error(f'function failed ,{WrongCredentialsException}')
            raise WrongCredentialsException('selected wrong user_role')
        if self.repo.get_by_condition(Customer,
                                      lambda query: query.filter(Customer.phone_no == customer.phone_no).all()):
            self.logger.logger.error(f'Function add_customer failed {DuplicateValueError}:{customer.phone_no}')
            raise DuplicateValueError('phone number already exists')
        if self.repo.get_by_condition(Customer, lambda query: query.filter(
                Customer.credit_card_no == customer.credit_card_no).all()):
            self.logger.logger.error(f'Function add_customer failed {WrongCredentialsException}: {customer.credit_card_no}')
            raise WrongCredentialsException('somefing wrong with the credit card number')
        if self.repo.get_by_condition(Customer, lambda query: query.filter(Customer.user_id == customer.user_id).all()):
            self.logger.logger.error(f'Function add_customer Failed {DuplicateValueError}')
            raise DuplicateValueError('user id already exists.')
        else:
            self.create_user(user)
            customer.id == None
            customer.user_id == user.id
            self.repo.add(customer)
            self.logger.logger.info('Function add_customer activated sucsessfuly.')
            return True
