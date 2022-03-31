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
from UserNotExistError import UserNotExist
from InvalidTokenError import InvalidToken





repo = DbRepo(local_session)
anonymuse_facade = AnonymousFacade()

@pytest.fixture(scope='function', autouse=True)
def reset_db():
    repo.init_db()



@pytest.fixture(scope='session')
def customer_facade_object():
    an_facade = anonymuse_facade.login('Yosi','053214')
    return an_facade




def test_update_customer(customer_facade_object):
    customer_facade_object.update_customer({'first_name': 'yosale'}, 1)
    check_customer = repo.get_by_id(Customer, 1)
    assert check_customer.first_name == 'yosale'

def test_negative_update(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.update_customer({'first_name':'test1',},'s')
    with pytest.raises(InvalidInput):
        customer_facade_object.update_customer({'first_name'== 'test2'},2)
    with pytest.raises(WrongCredentialsException):
        customer_facade_object.update_customer({'first_name':'test1',},4)
    with pytest.raises(InvalidToken):
        customer_facade_object.update_customer({'first_name':'test1',}, 2)




def test_add_ticket(customer_facade_object):
    customer_facade_object.add_ticket(Ticket(id= 11,flight_id = 1,customer_id = 1))
    check_ticket = repo.get_by_id(Ticket,11)
    assert check_ticket.flight_id == 1
    assert check_ticket.customer_id == 1

def test_fail_add_ticket(customer_facade_object):
    with pytest.raises(InvalidInput):
        new_ticket =Country(name= 'test1')
        customer_facade_object.add_ticket(new_ticket)
    with pytest.raises(FlightNotExist):
        customer_facade_object.add_ticket(Ticket(flight_id = 5,customer_id = 2))
    with pytest.raises(NoRemainingTicketsError):
        customer_facade_object.add_ticket(Ticket(flight_id = 3,customer_id = 2))
    with pytest.raises(InvalidInput):
        customer_facade_object.add_ticket(Ticket(flight_id = 2,customer_id = 7))
    with pytest.raises(InvalidToken):
        customer_facade_object.add_ticket(Ticket(id= 11,flight_id = 1,customer_id = 2))



def test_remove_ticket(customer_facade_object):
    customer_facade_object.remove_ticket(1)
    removed_ticket = repo.get_by_id(Ticket,1)
    assert removed_ticket == None

def test_fail_remove_ticket(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.remove_ticket('s')
    with pytest.raises(TicketNotExist):
        customer_facade_object.remove_ticket(5)
    with pytest.raises(InvalidToken):
        customer_facade_object.remove_ticket(2)

