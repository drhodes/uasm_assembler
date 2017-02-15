import sys
sys.path.append("../")

import ast
import gen
from symbol_table import SymbolTable

def test_assn1():
    a = gen.Generation("a=1\nb=2\n")
    symtab = a.symbol_pass(SymbolTable())
    assert symtab.num_symbols() == 2
    assert symtab.lookup("a") == ast.Number(1)
    assert symtab.lookup("b") == ast.Number(2)
    
def test_assn2():
    a = gen.Generation("a=1\nb=2\nb=3\n")
    symtab = a.symbol_pass(SymbolTable())
    assert symtab.num_symbols() == 2
    assert symtab.lookup("a") == ast.Number(1)
    assert symtab.lookup("b") == ast.Number(3)
    
def test_assn3():
    src = \
          '''
          x = a          
          a = c
          a = b
          b = c
          c = 1
          '''    
    a = gen.Generation(src)
    symtab = a.symbol_pass(SymbolTable())
    numNames = symtab.num_symbols()
    while True:
        a.replace_idents(symtab)
        symtab = a.symbol_pass(symtab)
        if symtab.num_symbols() == numNames:
            break
        numNames = symtab.num_symbols()
        
    assert symtab.resolveName('x') == ast.Number(1)
    assert symtab.resolveName('c') == ast.Number(1)
    assert symtab.resolveName('b') == ast.Number(1)
    assert symtab.resolveName('a') == ast.Number(1)
    assert symtab.num_symbols() == 4
    
def test_assn4():
    src = \
          '''
          a = b + 1
          b = c + 1
          c = 1
          '''
    a = gen.Generation(src)
    symtab = a.symbol_pass(SymbolTable())
    assert symtab.resolveName('c') == ast.Number(1)
    a.replace_idents(symtab)
    symtab = a.symbol_pass(symtab)
    assert symtab.resolveName('b') == ast.Number(2)
    a.replace_idents(symtab)
    symtab = a.symbol_pass(symtab)
    assert symtab.resolveName('a') == ast.Number(3)
    
def test_assn5():
    src = \
          '''
          x = a + b      
          a = b + 1
          b = c + 1
          c = 1
          '''    
    a = gen.Generation(src)
    symtab = a.symbol_pass(SymbolTable())
    numNames = symtab.num_symbols()
    while True:
        a.replace_idents(symtab)
        symtab = a.symbol_pass(symtab)
        if symtab.num_symbols() == numNames:
            break
        numNames = symtab.num_symbols()
        
    assert symtab.resolveName('c') == ast.Number(1)
    assert symtab.resolveName('b') == ast.Number(2)
    assert symtab.resolveName('a') == ast.Number(3)
    assert symtab.resolveName('x') == ast.Number(5)
    assert symtab.num_symbols() == 4

def test_assn6():
    src = \
          '''
          x = a + x
          a = b + 1
          b = c + 1
          c = 1
          x = 1
          x = 2
          '''    
    a = gen.Generation(src)
    symtab = a.symbol_pass(SymbolTable())
    numNames = symtab.num_symbols()
    while True:
        a.replace_idents(symtab)
        symtab = a.symbol_pass(symtab)
        if symtab.num_symbols() == numNames:
            break
        numNames = symtab.num_symbols()
        
    assert symtab.resolveName('c') == ast.Number(1)
    assert symtab.resolveName('b') == ast.Number(2)
    assert symtab.resolveName('a') == ast.Number(3)
    assert symtab.resolveName('x') == ast.Number(2)
    assert symtab.num_symbols() == 4
    
