import pytest
from AnonymousFacade import AnonymousFacade
from Users import User
from CustomerFacade import CustomerFacade
from DbRepo import DbRepo
from db_config import *
from WrongCredentialsException import WrongCredentialsException
from InvalidInput import InvalidInput
from AdministratorFacade import AdmininstratorFacade
from AirlineFacade import AirlineFacade
from Customers import Customer
from DuplicateValueError import DuplicateValueError




repo = DbRepo(local_session)






@pytest.fixture(scope='session')
def anonymusefacade_object():
    an_facade = AnonymousFacade()
    return an_facade

@pytest.fixture(scope='function', autouse=True)
def reset_db():
    repo.init_db()





def test_positive_login(anonymusefacade_object):
    assert  anonymusefacade_object.login('alonc', '053212')




def test_negative_login(anonymusefacade_object):
    with pytest.raises(InvalidInput):
      anonymusefacade_object.login('asd',12233442)
    with pytest.raises(InvalidInput):
        anonymusefacade_object.login(12,'12323332')
    with pytest.raises(WrongCredentialsException):
        anonymusefacade_object.login('alonc32','053212')
    with pytest.raises(WrongCredentialsException):
        anonymusefacade_object.login('alonc','1231222')

def test_add_customer(anonymusefacade_object):
    expected_customer = Customer(first_name='testot', last_name='testott', address='macho_city', phone_no='01212',
                                 credit_card_no='01121')
    expected_user = User(username='test1', password='test111', email='test@gmail.com', user_role=2)
    # expected_customer = Customer(first_name='testot', last_name='testott',address= 'macho_city',phone_no= '01212',credit_card_no= '01121',user_id= 7)
    anonymusefacade_object.add_customer(expected_user,expected_customer)
    assert repo.get_by_condition(Customer,lambda query:query.filter(Customer.first_name == 'testot')) !=None
    assert repo.get_by_condition(User,lambda query:query.filter(User.username == 'test1')) != None

def test_not_add_customer(anonymusefacade_object):
    with pytest.raises(DuplicateValueError):
        expected_customer = Customer(first_name='testot', last_name='testott', address='macho_city', phone_no='054456453',
                                     credit_card_no='01121')
        expected_user = User(username='test1', password='test111', email='test@gmail.com', user_role=2)
        anonymusefacade_object.add_customer(expected_user,expected_customer)
    with pytest.raises(DuplicateValueError):
        expected_customer = Customer(first_name='testot', last_name='testott', address='macho_city',
                                     phone_no='01212', credit_card_no='01121',user_id= 3)
        expected_user = User(username='test1', password='test111', email='test@gmail.com', user_role=2)
        anonymusefacade_object.add_customer(expected_user,expected_customer)
    with pytest.raises(InvalidInput):
        expected_customer = Customer(first_name='testot', last_name='testott', address='macho_city',
                                     phone_no='01212', credit_card_no='01121')
        expected_user = User(username='test1', password='test111', email='test@gmail.com', user_role=2)
        anonymusefacade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(WrongCredentialsException):
        expected_customer = Customer(first_name='testot', last_name='testott', address='macho_city',
                                     phone_no='01212', credit_card_no='52321231')
        expected_user = User(username='test1', password='test111', email='test@gmail.com', user_role=2)
        anonymusefacade_object.add_customer(expected_user, expected_customer)
