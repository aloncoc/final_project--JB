class WrongFlightError(Exception):
    def __init__(self,msg='such flight doesnt exist'):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'TicketNotFoundError:{self.msg}'
