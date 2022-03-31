from User_Roles import User_Role
from FacadeBase import FacadeBase
from Users import User
from Airline_Companies import Airline_Company
from  Administrators import Administrator
from Country import Country
from Customers import Customer
from Flights import Flight
from db_config import *
from DbRepo import DbRepo
from CustomerFacade import CustomerFacade
from Tickets import Ticket
from logger import Logger

from AirlineFacade import AirlineFacade
from AdministratorFacade import AdmininstratorFacade
repo = DbRepo(local_session)
logger = DbRepo(Logger.get_instance())

repo.init_db()
