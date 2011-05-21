registry = {}

def combinations_with_replacement(iterable, r):
  # combinations_with_replacement('ABC', 2) --> AA AB AC BB BC CC
  pool = tuple(iterable)
  n = len(pool)
  if not n and r:
    return
  indices = [0] * r
  yield tuple(pool[i] for i in indices)
  while True:
    for i in reversed(range(r)):
      if indices[i] != n - 1:
        break
    else:
      return
    indices[i:] = [indices[i] + 1] * (r - i)
    yield tuple(pool[i] for i in indices)

class MultiMethod(object):
    def __init__(self, name):
        self.name = name
        self.typemap = {}
    def __call__(self, *args):
        types = tuple(arg.__class__ for arg in args) # a generator expression!
        function = self.typemap.get(types)
        if function is None:
            #raise TypeError("no match: (%s, %s)" % (types))
            print "No collision defined for ({0}, {1})".format(*types)
            return False
        return function(*args)
    def register(self, types, function):
        # Commented out so we can override specifics
        #if types in self.typemap:
        #    raise TypeError("duplicate registration")
        self.typemap[types] = function

def SymmetricTravel(*types):
  return _multimethod(*types, symmetric=True)

def UnidirectionalTravel(*types, **kwargs):
  return _multimethod(*types, **kwargs)

def _multimethod(*types, **kwargs):
    def register(function):
        name = function.__name__
        mm = registry.get(name)
        if mm is None:
          mm = registry[name] = MultiMethod(name)
        if kwargs.get('symmetric', False):
            for comb in combinations_with_replacement(types, 2):
              print comb
              mm.register(comb, function)
        elif kwargs.get('rootto', False):
          root , t = types[:1], types[1:]
          for comb in t:
            mm.register(root+(comb,), function)
        elif kwargs.get('rootfrom', False):
          root , t = types[:1], types[1:]
          for comb in t:
            mm.register((comb,)+root, function)
        else:
          mm.register(types, function)
        return mm
    return register

if __name__ == "__main__":
  #@multimethod(int,float, symmetric=True)
  #def bar(a,b):
  #    return a*b

  #@multimethod(int, str)
  #def bar(a, b):
  #  return "%s:%s" % (b, a)

  #@multimethod(int, float, str, rootto=True)
  #def bar(a, b):
  #  return a, b

  @UnidirectionalTravel(int, float, str, tuple, rootfrom=True)
  def bar(a,b):
    return a, b

  """print bar(1,2.0)
  print bar(2.0,1)
  print bar(1,"hello")
  try:
    print bar("hello", 1) # raise Error
  except Exception, e:
    print e"""
  print bar(1.0,1)
  print bar(";",1)
