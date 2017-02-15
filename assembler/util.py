
class Seq(list):
    def __init__(self, *args):
        list.__init__(self, args)
        self.parse_method = None
    def set_parse_method(self, pm):
        self.parse_method = pm
    def eval(self):
        return self
    def is_seq(self):
        return True
    def is_epsilon(self):
        return False

    def pretty(self, depth):
        for x in self: x.pretty(depth+1)
    
    def augment_symbol_table(self, symtab):
        for obj in self:
            symtab = obj.augment_symbol_table(symtab)
        return symtab

    def replace_idents(self, symtab):
        for obj in self:
            obj.replace_idents(symtab)                
            
    def generate(self, symtab):
        result = []
        for obj in self:
            result += obj.generate(symtab)
        return result 
    
def die(*args):
    if len(args) == 0:
        raise Exception("planned demise")
    else:
        raise Exception(args[0])
    
def same_type(x, y):
    return x.__class__.__name__ == y.__class__.__name__

def is_token(x):
    return x.__class__.__name__ == "Token"

def type_is(x, s):
    return x.__class__.__name__ == s

def is_number(x): return type_is(x, "Number")
def is_ident(x): return type_is(x, "Ident")


def deadcode():
    raise Exception("Supposed deadcode encountered")

def reduce_seq(xs):
    if not type_is(xs, "Seq"):
        raise Exception("No lists allowed, the parser must use Seqs everywhere")
    ''' 
    if a list contains only a list, then unwrap it
    '''    
    if len(xs) == 1:
        if type_is(xs[0], "Seq"):
            return reduce_seq(xs[0])
    return xs

def deflag(p):
    ''' 
    if a string starts with a ~, remove it
    >>> deflag("~asdf")
    asdf
    >>> deflag("~zxcv")
    zxcv
    '''
    if p.startswith("~"):
        return True, p[1:]
    return False, p

def unnest(xs):
    ''' flatten a list that looks like
    [x, [y, [z]]]
    '''
    if len(xs) == 0: return []
    if len(xs) == 1: return xs
    return [xs[0]] + unnest(xs[1])


def echo(fn):
    "Returns a traced version of the input function."
    from itertools import chain
    def wrapped(*v, **k):
        name = fn.__name__
        print "%s(%s)" % (
            name, ", ".join(map(repr, chain(v, k.values()))))
        return fn(*v, **k)
    return wrapped

