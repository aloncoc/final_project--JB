class InvalidToken(Exception):
    def __init__(self,msg='Token not match.'):
        self.msg = msg
        super().__init__(self.msg)
    def __repr__(self):
        return f'InvalidToken {self.msg}'
