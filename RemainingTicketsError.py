class NoRemainingTicketsError(Exception):
  def __init__(self,msg='sryy we are out of tickets for that flight.'):
      self.msg = msg
      super().__init__(self.msg)
      
  def __str__(self):
      return f'NoRemainingTicketsError {self.msg}'
