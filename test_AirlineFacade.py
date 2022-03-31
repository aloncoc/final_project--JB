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
from AirlineFacade import AirlineFacade
from DbRepo import DbRepo
from db_config import *
from AnonymousFacade import AnonymousFacade
import pytest
from CountryNotExistError import CountryNotExist
from UserNotExistError import UserNotExist
from InvalidUser_roleError import Invalid_User_role
from FlightNotExistError import FlightNotExist
from CountryNotExistError import CountryNotExist
from Flights import Flight
import datetime
from DepartureTimeError import DepartureTimeError
from InvalidTokenError import InvalidToken






repo = DbRepo(local_session)
anonymuse_facade = AnonymousFacade()

@pytest.fixture(scope='session')
def airline_facade_object():
    an_facade = anonymuse_facade.login('Dan','053217')
    return an_facade

@pytest.fixture(scope='function', autouse=True)
def reset_db():
    repo.init_db()

def test_update_ariline(airline_facade_object):
    airline_facade_object.update_airline({'name':'klas'},2)

def test_fail_update_airline(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.update_airline({'name': 'klas'}, '2')
    with pytest.raises(InvalidInput):
        airline_facade_object.update_airline({'name'== 'klas'}, 2)
    with pytest.raises(AirlineNotFound):
        airline_facade_object.update_airline({'name': 'klas'}, 5)
    with pytest.raises(InvalidToken):
        airline_facade_object.update_airline({'name': 'klas'}, 1)



def test_update_flight(airline_facade_object):
    airline_facade_object.update_flight({'remaining_tickets': 32},2)

def test_fail_update_flight(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.update_flight({'remaining_tickets': 20}, '2')
    with pytest.raises(InvalidInput):
        airline_facade_object.update_flight({'remaining_tickets'== 20}, 2)
    with pytest.raises(FlightNotExist):
        airline_facade_object.update_flight({'remaining_tickets': 20}, 5)
    with pytest.raises(InvalidToken):
        airline_facade_object.update_flight({'remaining_tickets': 23}, 1)

def test_add_flight(airline_facade_object):
    airline_facade_object.add_flight(Flight(id =11,airline_company_id=2, origin_country_id=1,
                         destination_country_id=2, departure_time=datetime.datetime(2022, 1, 30, 15, 0, 0),
                         landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                         remaining_tickets=150))
    assert repo.get_by_id(Flight,11) != None


def test_fail_add_flight(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.add_flight(Country(name='china'))
    with pytest.raises(DuplicateValueError):
        airline_facade_object.add_flight(Flight(id=1, airline_company_id=2, origin_country_id=1,
                                                destination_country_id=2,
                                                departure_time=datetime.datetime(2022, 1, 30, 15, 0, 0),
                                                landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                                                remaining_tickets=150))
    with pytest.raises(AirlineNotFound):
        airline_facade_object.add_flight(Flight(id=11, airline_company_id=12, origin_country_id=1,
                                                destination_country_id=2,
                                                departure_time=datetime.datetime(2022, 1, 30, 15, 0, 0),
                                                landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                                                remaining_tickets=150))
    with pytest.raises(CountryNotExist):
        airline_facade_object.add_flight(Flight(id=11, airline_company_id=2, origin_country_id=12,
                                                destination_country_id=2,
                                                departure_time=datetime.datetime(2022, 1, 30, 15, 0, 0),
                                                landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                                                remaining_tickets=150))
    with pytest.raises(CountryNotExist):
        airline_facade_object.add_flight(Flight(id=11, airline_company_id=2, origin_country_id=1,
                                                destination_country_id=15,
                                                departure_time=datetime.datetime(2022, 1, 30, 15, 0, 0),
                                                landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                                                remaining_tickets=150))
    with pytest.raises(InvalidInput):
        airline_facade_object.add_flight(Flight(id=11, airline_company_id=2, origin_country_id=1,
                                                destination_country_id=2,
                                                departure_time=datetime.datetime(2022, 1, 30, 15, 0, 0),
                                                landing_time=datetime.datetime(2021, 1, 31, 12, 0, 0),
                                                remaining_tickets=150))
    with pytest.raises(InvalidInput):
        airline_facade_object.add_flight(Flight(id=11, airline_company_id=2, origin_country_id=1,
                                                destination_country_id=2,
                                                departure_time=datetime.datetime(2022, 1, 30, 15, 0, 0),
                                                landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                                                remaining_tickets=-2))
    with pytest.raises(InvalidInput):
        airline_facade_object.add_flight(Flight(id=11, airline_company_id=2, origin_country_id=1,
                                                destination_country_id=1,
                                                departure_time=datetime.datetime(2022, 1, 30, 15, 0, 0),
                                                landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                                                remaining_tickets=150))
    with pytest.raises(InvalidToken):
        airline_facade_object.add_flight(Flight(id =11,airline_company_id=1, origin_country_id=1,
                         destination_country_id=2, departure_time=datetime.datetime(2022, 1, 30, 15, 0, 0),
                         landing_time=datetime.datetime(2022, 1, 31, 12, 0, 0),
                         remaining_tickets=150))

def test_remove_flight(airline_facade_object):
    airline_facade_object.remove_flight(2)

def test_not_remove_flight(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.remove_flight('2')
    with pytest.raises(InvalidInput):
        airline_facade_object.remove_flight(11)
    with pytest.raises(InvalidToken):
        airline_facade_object.remove_flight(1)
