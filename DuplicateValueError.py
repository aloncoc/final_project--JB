class DuplicateValueError(Exception):
    def __init__(self,msg='cannot use same value twice in the same class'):
        self.msg = msg
        super().__init__(self.msg)
    def __repr__(self):
        return f'DuplicateValueError {self.msg}'
