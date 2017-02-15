import sys
sys.path.append("../")

from symbol_table import SymbolTable

class MacroExec(object):
    '''A MacroExec object constructs a local symbol table (LST) every time
    the macro is called.

    When a macro is called, it builds a LST.  If a symbol is
    referenced that isn't contained in the LST then the macro looks to
    the global symbol table (GST).  The macro can reference values
    from the GST, but it can not bind new values to the GST.  Macros
    bind values only to LST, so a method is used for all binding that
    takes care to obey this invarient.

    '''    
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body
        self.lst = SymbolTable()

    def num_args(self):
        return len(self.args)
        
    def bind(self, exprList):
        '''bind arguments to the local symbol table'''        
        assert len(exprList) == len(self.args)
        bindPairs = zip(self.args, [e.eval() for e in exprList])

        # this mutates self.lst making for sad things to happen next
        # time this macro is invoked. or maybe not, maybe it simply
        # clobbers the old bindings?
        self.lst = SymbolTable()
        self.lst.bind(bindPairs)

    def generate(self, symtab):
        ''' generate a sequence of bytes '''
        # copy the macro body so the Ident nodes are preserved for the
        # next invocation of this macro.
        # import copy
        # ast = copy.deepcopy(self.body)
        ast = self.body
        
        ast.replace_idents(self.lst)
        ast.replace_idents(symtab)
        
        return ast.generate(symtab)


    
