import pytest
from AnonymousFacade import AnonymousFacade
from Users import User
from DbRepo import DbRepo
from db_config import *
from WrongCredentialsException import WrongCredentialsException
from InvalidInput import InvalidInput
from Customers import Customer
from DuplicateValueError import DuplicateValueError
from FacadeBase import FacadeBase
from PasswordTooShort import PasswordTooShortError
from Administrators import Administrator
from CustomerFacade import CustomerFacade
from Tickets import Ticket
from Country import Country
from FlightNotExistError import FlightNotExist
from NoRemainingTicketsError import NoRemainingTicketsError
from TicketNotExistError import TicketNotExist
from InvalidUser_roleError import Invalid_User_role
from Airline_Companies import Airline_Company
from AirlineNotFoundError import AirlineNotFound
from InvalidTokenError import InvalidToken
from  UserAlreadyExistError import UserAlreadyExitsError
from CountryNotExistError import CountryNotExist






repo = DbRepo(local_session)
anonymuse_facade = AnonymousFacade()

@pytest.fixture(scope='session')
def admin_facade_object():
    an_facade = anonymuse_facade.login('alonc','053212')
    return an_facade

@pytest.fixture(scope='function', autouse=True)
def reset_db():
    repo.init_db()

def test_add_admin(admin_facade_object):
    new_admin = Administrator(id=3,first_name='test1',last_name='test2',user_id= 7)
    admin_facade_object.add_admin(new_admin)
    assert new_admin != None

def test_fail_add_admin(admin_facade_object):
    with pytest.raises(InvalidInput):
        admin_facade_object.add_admin(Country(name='budapest'))
    with pytest.raises(DuplicateValueError):
        admin_facade_object.add_admin(Administrator(id=1,first_name='test1',last_name='test2',user_id= 7))
    with pytest.raises(DuplicateValueError):
        admin_facade_object.add_admin(Administrator(id=3, first_name='test1', last_name='test2', user_id=1))
    with pytest.raises(Invalid_User_role):
        admin_facade_object.add_admin(Administrator(id=3, first_name='test1', last_name='test2', user_id=4))
    with pytest.raises(WrongCredentialsException):
        admin_facade_object.add_admin(Administrator(id=3, first_name='test1', last_name='test2', user_id=9))

def test_remove_airline(admin_facade_object):
    admin_facade_object.remove_airline(2)
    assert repo.get_by_id(Airline_Company,2) == None

def test_fail_remove_airline(admin_facade_object):
    with pytest.raises(InvalidInput):
        admin_facade_object.remove_airline('2')
    with pytest.raises(AirlineNotFound):
        admin_facade_object.remove_airline(5)

def test_add_customer(admin_facade_object):
    expected_customer = Customer(first_name='testa', last_name='testo', address='testat 31',
                                  phone_no='test053221', credit_card_no='test022111', user_id=9)
    expected_user = User(username='test3311', password='test2211', email='test@gmail.com', user_role=2)
    admin_facade_object.add_customer(expected_user,expected_customer)
    assert expected_user != None
    assert expected_customer != None

def test_not_add_customer(admin_facade_object):
    with pytest.raises(InvalidInput):
       expected_customer = Customer(first_name='testa', last_name='testo', address='testat 31',
                                 phone_no='test053221', credit_card_no='test022111', user_id=5)
       expected_user = User(username='test3311', password='test2211', email='test@gmail.com', user_role=2)
       admin_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(DuplicateValueError):
        expected_customer = Customer(first_name='testa', last_name='testo', address='testat 31',
                                     phone_no='0544564221', credit_card_no='test022111', user_id=9)
        expected_user = User(username='test3311', password='test2211', email='test@gmail.com', user_role=2)
        admin_facade_object.add_customer(expected_user, expected_customer)
    with pytest.raises(WrongCredentialsException):
        expected_customer = Customer(first_name='testa', last_name='testo', address='testat 31',
                                     phone_no='test053221', credit_card_no='52321333', user_id=9)
        expected_user = User(username='test3311', password='test2211', email='test@gmail.com', user_role=2)
        admin_facade_object.add_customer(expected_user, expected_customer)
    with pytest.raises(Invalid_User_role):
        expected_customer = Customer(first_name='testa', last_name='testo', address='testat 31',
                                     phone_no='test053221', credit_card_no='test022111', user_id=9)
        expected_user = User(username='test3311', password='test2211', email='test@gmail.com', user_role=3)
        admin_facade_object.add_customer(expected_user, expected_customer)

def test_remove_customer(admin_facade_object):
    expected_user = User(username='test3311', password='test2211', email='test@gmail.com', user_role=2)
    expected_customer = Customer(first_name='tes12', last_name='testo3', address='testat 313',
                                 phone_no='test05321', credit_card_no='test0211', user_id=expected_user.id)
    admin_facade_object.add_customer(expected_user, expected_customer)
    admin_facade_object.remove_customer(3)
    assert repo.get_by_id(Customer,3) == None

def test_not_remove_customer(admin_facade_object):
    with pytest.raises(InvalidInput):
        admin_facade_object.remove_customer('4')
    with pytest.raises(WrongCredentialsException):
        admin_facade_object.remove_customer(5)












def test_add_airline(admin_facade_object):
    ex_airline =Airline_Company(name='ac_airlines',country_id=1,user_id=9)
    ex_user = User(username='test33', password='test13211', email='tesla@walla.com', user_role=3)
    admin_facade_object.add_airline(ex_airline,ex_user)
    airline = repo.get_by_id(Airline_Company,3)
    assert airline.name == 'ac_airlines'

def test_not_add_ariline(admin_facade_object):
    with pytest.raises(InvalidInput):
        ex_airline = Airline_Company(name='ac_airlines', country_id=1, user_id=9)
        ex_user = User(username='test33', password='test13211', email='tesla@walla.com', user_role=3)
        admin_facade_object.add_airline(ex_user, ex_airline)
    with pytest.raises(DuplicateValueError):
        ex_airline = Airline_Company(id=1,name='ac_airlines', country_id=1, user_id=9)
        ex_user = User(username='test33', password='test13211', email='tesla@walla.com', user_role=3)
        admin_facade_object.add_airline(ex_airline, ex_user)
    with pytest.raises(DuplicateValueError):
        ex_airline = Airline_Company(name='elal', country_id=1, user_id=9)
        ex_user = User(username='test33', password='test13211', email='tesla@walla.com', user_role=3)
        admin_facade_object.add_airline(ex_airline, ex_user)
    with pytest.raises(DuplicateValueError):
        ex_airline = Airline_Company(name='ac_airlines', country_id=1, user_id=6)
        ex_user = User(username='test33', password='test13211', email='tesla@walla.com', user_role=3)
        admin_facade_object.add_airline(ex_airline, ex_user)
    with pytest.raises(CountryNotExist):
        ex_airline = Airline_Company(name='ac_airlines', country_id=5, user_id=9)
        ex_user = User(username='test33', password='test13211', email='tesla@walla.com', user_role=3)
        admin_facade_object.add_airline(ex_airline, ex_user)
    with pytest.raises(Invalid_User_role):
        ex_airline = Airline_Company(name='ac_airlines', country_id=1, user_id=9)
        ex_user = User(username='test33', password='test13211', email='tesla@walla.com', user_role=2)
        admin_facade_object.add_airline(ex_airline, ex_user)
