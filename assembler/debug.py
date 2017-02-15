import common



# http://wordaligned.org/articles/echo
def echo(fn):
    if not common.DEBUG: return fn
    "Returns a traced version of the input function."
    from itertools import chain
    def wrapped(*v, **k):
        name = fn.__name__
        print "%s(%s)" % (
            name, ", ".join(map(repr, chain(v, k.values()))))
        return fn(*v, **k)
    return wrapped
