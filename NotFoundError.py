class NotFoundError(Exception):
    def __init__(self,msg='such item not exist.'):
        self.msg = msg
        super.__init__(self.msg)
    def __repr__(self):
        return f'NotFoundError {self.msg}'
