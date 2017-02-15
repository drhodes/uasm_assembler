import sys
sys.path.append("../")

from lexer import lexer
from symbol_table import SymbolTable
import parse
import gen

# def eval_macro(text, testFunc):
#     p = parse.build_parser(lexer.lex_string(text))
#     result = p.parse("TopLevel", text)
#     assert False

#     r = result.eval()
#     if testFunc(r):
#         pass
#     else:
#         print "--------------------------------------------"
#         print "               rule: %s" % "TopLevel"
#         print "               text: %s" % text
#         print "                got: %s" % r
#         print ('r', r, type(r))
#         assert testFunc(r)

def test(): pass

# macros need to go into the symbol_table, maybe a separate table.
# WORD = fn(x): x % 0x100 (x >> 8) % 0x100

def assemble_macro(src):
    a = gen.Generation(src)
    symtab = a.symbol_pass(SymbolTable())
    numNames = symtab.num_symbols()
    while True:
        a.replace_idents(symtab)
        symtab = a.symbol_pass(symtab)
        if symtab.num_symbols() == numNames:
            break
        numNames = symtab.num_symbols()
    return symtab

def test_eval_macro_0():
    s = \
        ''' 
        r0 = 0
        r1 = 1
        .macro ID(x) x
        '''
    assemble_macro(s)

    
def test_eval_macro_1():
    s = \
        ''' 
        r0 = 0
        r1 = 1
        .macro ID(x) x
        ID(r0)
        '''
    symtab = assemble_macro(s)
    # assert symtab.lookup('a') == ast.Number(0)
    
