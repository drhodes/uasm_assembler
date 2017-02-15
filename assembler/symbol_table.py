import util

class SymbolTable(object):
    def __init__(self, *args):
        self.store = {}
        self.macros = {}
        
    def insert(self, name, val):
        assert type(name) == str
        self.store[name] = val

    def insert_macro(self, name, mac):
        assert type(name) == str
        self.macros[(name, mac.num_args())] = mac
        
    def lookup(self, name):
        assert type(name) == str
        return self.store[name]

    def clear(self):
        for k in self.store:
            self.store[k] = None
        for k in self.macros:
            self.macros[k] = None
    
    def lookup_macro(self, name, num_args):
        assert type(name) == str
        return self.macros[(name, num_args)] 
    
    def num_symbols(self):
        return len(self.store)
    
    def __contains__(self, name):
        assert type(name) == str
        return name in self.store

    def bind(self, exprList):
        for (k, v) in exprList:
            self.insert(k.tok, v)
        # print self.store
    
    def resolveName(self, name):        
        '''try to resolve a name in the symbol table'''
        assert type(name) == str

        if name in self.store:
            # check if the symbol's value is not an Ident
            val = self.store[name]
            if util.type_is(val, "Number"):                
                # the value is concrete and resolves.
                return val
            elif util.type_is(val, "Ident"):                
                # else, then chase that rabbit.
                return self.resolveName(val.name())
            else:
                # otherwise what is it? Dunno, needs more eval.
                return None            
        else:
            # couldn't find the symbol
            return None
            raise Exception("Couldn't find symbol: %s" % name)
        
    def __repr__(self):
        msg = "<SYMBOL-TABLE (idents %s) (macros %s)>"
        return msg % (self.store.items(), self.macros.items())
