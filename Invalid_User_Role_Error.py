class Invalid_User_role(Exception):
    def __init__(self,msg='Invalid user_role has been selected.'):
        self.msg = msg
        super().__init__(self.msg)
    def __repr__(self):
        return f'Invalid_User_role {self.msg}'
