import typ

@typ.typ(y=int,x=int)
class Z(object):
  @typ.typ(self='cls.Z', xx=int, yy=int)
  def __init__(self, xx, yy):
    self.x = xx
    self.y = yy

  @typ.typ(self='cls.Z', xxx=int)
  def sum(self, xxx):
    """
    >>> Z(1,2).sum(3)
    6
    """
    return self.x + self.y + xxx


