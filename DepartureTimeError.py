class DepartureTimeError(Exception):
    def __init__(self,msg='departure or landing time invalid.'):
        self.msg = msg
        super().__init__(self.msg)
    def __repr__(self):
        return f'DepartureTimeError {self.msg}'
