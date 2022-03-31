class UserNotExist(Exception):
    def __init__(self,msg='user_id not exist.'):
        self.msg = msg
        super().__init__(self.msg)
    def __repr__(self):
        return f'UserNotExist {self.msg}'
