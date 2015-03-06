import typ
class MyClass:
  @typ.typ(a=[int])
  def func2(self,a):
    """
    >>> x = MyClass()
    >>> x.func2([4])
    False
    >>> x.func2([8])
    True
    """
    if a[0] > 6:
        return True
    return False

