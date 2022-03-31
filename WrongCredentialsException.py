class WrongCredentialsException(Exception):
    def __init__(self, msg='Your username or password is wrong.'):
        self.msg = msg
        super().__init__(self.msg)

    def __repr__(self):
        return f'WrongCredentialsException {self.msg}'
