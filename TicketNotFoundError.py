from Tickets import Ticket

class TicketNotFoundError(Exception):
    def __init__(self,ticket_id,msg='there isnt such ticket'):
        self.ticket_id = ticket_id
        self.msg = msg
        super.__init__(self.msg)

    def __str__(self):
        return f'TicketNotFoundError:{self.msg}'
    
