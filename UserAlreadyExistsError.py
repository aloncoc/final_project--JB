class UserAlreadyExitsError():
    def __init__(self,msg='User already exits'):
        self.msg = msg
        super().__init__(self.msg)
        
    def __str__(self):
        return f'UserAlreadyExitsError {self.msg}'
