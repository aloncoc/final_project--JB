class TicketNotExist(Exception):
    def __init__(self, msg='ticket not exist.'):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'TicketNotExist {self.msg}'
