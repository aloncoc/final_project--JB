class NoMoreTicketsForFlightsError(Exception):
    def __init__(self,msg='No remaining tickets for this flight.'):
        self.msg = msg
        super.__init__(self.msg)
    def __repr__(self):
        return f'NoMoreTicketsForFlightError {self.msg}'
