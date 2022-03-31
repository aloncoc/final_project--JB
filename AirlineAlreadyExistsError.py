class AlrineAlreadyExists(Exception):
    def __init__(self,msg='Airline with such details does not exist.'):
        self.msg = msg
        super.__init__(self.msg)
    def __repr__(self):
        return f'AirlineNotFound {self.msg}'
