import sys
sys.path.append("../")

from lexer import lexer
import parse

class Generation(object):
    def __init__(self, src):
        self.parsers = []
        self.ast = None

        self.parsers = []
        
        parser = parse.build_parser(lexer.lex_string(src))
        self.ast = parser.parse_top()

    def replace_idents(self, symtab):
        '''this mutates self.ast. Recurse over ast, upon ident, look it up in
        the symbol table and if found replace the ident with the value
        from the symbol table.

        '''
        self.ast.replace_idents(symtab)
        
    def symbol_pass(self, symtab):
        return self.ast.augment_symbol_table(symtab)

    def generate(self, symtab):
        return self.ast.generate(symtab)
