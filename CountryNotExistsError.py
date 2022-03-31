class CountryNotExist(Exception):
    def __init__(self,msg='Country_id not exist.'):
        self.msg = msg
        super().__init__(self.msg)
    def __repr__(self):
        return f'CountryNotExist {self.msg}'
