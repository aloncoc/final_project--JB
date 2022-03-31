class PasswordTooShortError(Exception):
    def __init__(self,msg='Password too short'):
        self.msg = msg
        super().__init__(self.msg)
        
    def __str__(self):
        return f'PasswordTooShort {self.msg}'
