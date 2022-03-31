from datetime import datetime
from User_Roles import User_Role
from Tickets import Ticket
from Flights import Flight
from DbRepo import DbRepo
from Customers import Customer
from logger import Logger
from Users import User
from FacadeBase import FacadeBase
from NoRemainingTicketsError import NoRemainingTicketsError
from NoMoreTicketsForFlights import NoMoreTicketsForFlightsError
from WrongCredentialsException import WrongCredentialsException
from InvalidInput import InvalidInput
from WrongFlightError import WrongFlightError
from DuplicateValueError import DuplicateValueError
from FlightNotExistError import FlightNotExist
from TicketNotExistError import TicketNotExist
from UserNotExistError import UserNotExist
from InvalidTokenError import InvalidToken


class CustomerFacade(FacadeBase):

    def __init__(self,login_token):
        super().__init__()
        self.login_token = login_token

    def update_customer(self, customer, customer_id):
        self.logger.logger.debug(f'Attempting to update customer #{customer_id}...')
        if not isinstance(customer_id, int):
            self.logger.logger.error(f'{InvalidInput} - Input must be an integer!')
            raise InvalidInput('Input must be an integer!')
        elif not isinstance(customer, dict):
            self.logger.logger.error(f'{InvalidInput} - Input must be an integer!')
            raise InvalidInput('input must be a dictionary!')
        else:
            customer_object = self.repo.get_by_id(Customer, customer_id)
            if customer_object == None:
                self.logger.logger.error(f'{WrongCredentialsException} - Customer #{customer_id} was not found!')
                raise WrongCredentialsException(f'customer with id {customer_id} not exist')

            else:
               if self.login_token.id != customer_object.id:
                 self.logger.logger.error(f'{InvalidToken} - you cannot edit other customers!')
                 raise InvalidToken()

               else:
                        self.logger.logger.info(f'Customer #{customer_id} Updated!')
                        self.repo.update_by_id(Customer, Customer.id, customer_id, customer)






    def add_ticket(self,ticket):
        self.logger.logger.debug('Attepmting to activate add_ticket function')
        if not isinstance(ticket, Ticket):
            self.logger.logger.error(f'Function add_ticket failed {InvalidInput}')
            raise InvalidInput('ticket must be instance of class Ticket')
        flight = self.get_flight_by_id(ticket.flight_id)
        if flight == None:
            self.logger.logger.error(f'Function add_ticket failed,{FlightNotExist}')
            raise FlightNotExist(f'flight with id: {ticket.flight_id} not exist. ')
        if flight.remaining_tickets <= 0 :
            self.logger.logger.error(f'Function add_ticket failed ,{NoRemainingTicketsError}')
            raise NoRemainingTicketsError('no remaining tickets left for this flight.')
        check_customer = self.repo.get_by_id(Customer,ticket.customer_id)
        if check_customer == None:
            self.logger.logger.error(f'{InvalidInput} function failed customer not exists.')
            raise InvalidInput(f'customer with id : {ticket.customer_id} not exist.')
        else:
            if self.login_token.id != check_customer.id :
                self.logger.logger.error(f'{InvalidToken} - you cannot edit for other customers!')
                raise InvalidToken()

            else:
                self.repo.update_by_id(Flight, Flight.remaining_tickets, ticket.flight_id,
                                       {Flight.remaining_tickets: flight.remaining_tickets - 1})
                self.repo.add(ticket)
                self.logger.logger.info('Function add_ticket has sucsessfuly activated.')

    def remove_ticket(self,ticket):
        self.logger.logger.debug(f'Attempting to remove ticket #{ticket}...')
        if not isinstance(ticket, int):
            self.logger.logger.error(f'{InvalidInput} - Input must be an integer!!')
            raise InvalidInput('Input must be an integer!')
        elif self.repo.get_by_id(Ticket, ticket) == None:
            self.logger.logger.error(f'{TicketNotExist} - Ticket #{ticket} was not found!')
            raise TicketNotExist
        else:
            ticket_delete = self.repo.get_by_id(Ticket, ticket)
            customer = self.repo.get_by_id(Customer, ticket_delete.customer_id)
            if self.login_token.id != customer.id:
                self.logger.logger.error(f'{InvalidToken} - you cannot edit for other customers!')
                raise InvalidToken
            else:
                flight = self.get_flight_by_id(ticket_delete.flight_id)
                self.repo.update_by_id(Flight, Flight.id, flight.id,
                                       {'remaining_tickets': flight.remaining_tickets + 1})
                self.repo.delete_by_id(Ticket, Ticket.id, ticket)
                self.logger.logger.info(f'Ticket #{ticket} Deleted!')


    def get_tickets_by_customer_id(self,customer_id):
        if not isinstance(customer_id, int):
            print('Function failed, customer_id must be an integer.')
            return
        return self.repo.get_by_condition(Ticket,lambda query : query.filter(Ticket.customer_id == customer_id).all())
