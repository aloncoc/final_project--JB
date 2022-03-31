import pytest
from AdministratorFacade import AdmininstratorFacade
from AirlineFacade import AirlineFacade
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
from InvalidUser_roleError import Invalid_User_role



repo = DbRepo(local_session)

@pytest.fixture(scope='function', autouse=True)
def reset_db():
    repo.init_db()

@pytest.fixture(scope='session')
def facadebase_object():
    an_facade = AnonymousFacade()
    return an_facade

def test_create_user(facadebase_object):
    new_user = User(username='test2',password='test123',email='test@gmail.com',user_role=2)
    facadebase_object.create_user(new_user)
    assert repo.get_by_condition(User,lambda query: query.filter(User.username == 'test2')) != None

def test_negative_create_user(facadebase_object):
    with pytest.raises(InvalidInput):
        new_user = Administrator(first_name= 'asda',last_name= 'asda2',user_id= 2)
        facadebase_object.create_user(new_user)
    with pytest.raises(WrongCredentialsException):
        new_user = User(username='alonc',password='test123',email='test@gmail.com',user_role=2)
        facadebase_object.create_user(new_user)
    with pytest.raises(DuplicateValueError):
        new_user = User(username='test2',password='test123',email='alonc@gmail.com',user_role=2)
        facadebase_object.create_user(new_user)
    with pytest.raises(PasswordTooShortError):
        new_user = User(username='test2',password='2123',email='test@gmail.com',user_role=2)
        facadebase_object.create_user(new_user)
    with pytest.raises(Invalid_User_role):
        new_user = User(username='test2', password='test123', email='test@gmail.com', user_role=4)
        facadebase_object.create_user(new_user)

