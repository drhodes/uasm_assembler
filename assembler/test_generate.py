import sys
sys.path.append("../")

import gen
import ast
import util
from symbol_table import SymbolTable

def do_test_generate_file(srcFile, expected):
    src = open("./tests/generate/" + srcFile + ".uasm").read()
    do_test_generate(src, expected)
    
def do_test_generate(src, expected):
    a = gen.Generation(src)
    symtab = a.symbol_pass(SymbolTable())
    numNames = symtab.num_symbols()
    while True:
        a.replace_idents(symtab)
        symtab = a.symbol_pass(symtab)
        if symtab.num_symbols() == numNames:
            break
        numNames = symtab.num_symbols()
        
    words = a.generate(symtab)
    for w in words:
        print w
    
    if words != expected:       
        print "GENERATED:", words
        print "EXPECTED :", expected
        # print a.ast
        # a.ast.pretty(0)
        util.die()

def num_inst(x): return ast.AssemblerInst("NUMBER", ast.Number(x))
        
# def test_sandbox_1():
#     do_test_generate_file("sandbox1", map(num_inst, [1,1,1,1,2,2,2,2]))
# def test_sandbox_2():
#     do_test_generate_file("sandbox2", map(num_inst, [2,2,4,4]))
# def test_sandbox_3():
#     do_test_generate_file("sandbox3", map(num_inst, [2,2,4,4,8,8]))
# def test_sandbox_4():
#     do_test_generate_file("sandbox4", [])
# def test_sandbox_5():
#     do_test_generate_file("sandbox5", [num_inst(6)])
# def test_sandbox_6():
#     do_test_generate_file("sandbox6", map(num_inst, [0xef, 0xbe]))
# def test_sandbox_7():
#     do_test_generate_file("sandbox7", map(num_inst, [0xef, 0xbe, 0xad, 0xde]))

def test_sandbox_8():
    temp = [ast.AssemblerInst("DOT_ALIGN", ast.Number(4))]
    temp += map(num_inst, [0x00, 0x10, 0x61, 0x80])
    do_test_generate_file("sandbox8", temp)

def test_sandbox_proc_1():
    do_test_generate(".align 4",
                     [ast.AssemblerInst("DOT_ALIGN", ast.Number(4))])

    
# this test needs to go into testing for the final byte stream.
# def test_sandbox_dot_1():
#     do_test_generate(". = .",
#                      [ast.AssemblerInst("DOT_ASSN", None)])

# def test_sandbox_9():
#     do_test_generate_file("beta", []) 

def test_label_1():
    do_test_generate_file("label1",
                          [ast.AssemblerInst("LABEL", "mylabel")])

