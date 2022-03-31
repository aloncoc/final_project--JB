class FlightNotExist(Exception):
    def __init__(self, msg='this flight not exist'):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'FlightNotExist {self.msg}'
