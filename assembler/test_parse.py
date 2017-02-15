import os, sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from lexer import lexer
import parse

def parse_test(rule, s):
    p = parse.build_parser(lexer.lex_string(s))
    p.parse(rule, s)
    
def test_ast_lit_num_dec():
    parse_test("LitNum", "42")
def test_ast_lit_num_hex():
    parse_test("LitNum", "0x2a")
def test_ast_lit_num_bin():
    parse_test("LitNum", "0b101010")
def test_ast_ident_1():
    parse_test("Ident", "asdf")
def test_ast_ident_dot():
    parse_test("Ident", ".")
def test_parse_test_ident_sep_comma():    
    parse_test("IdentSepComma", "a")    
def test_parse_test_ident_sep_comma_Multi():    
    parse_test("IdentSepComma", "a, a, a, a, a")
def test_parse_test_ident_list():    
    parse_test("IdentList", "()")    
def test_parse_test_ident_list1():    
    parse_test("IdentList", "(a)")    
def test_parse_test_ident_list2():        
    parse_test("IdentList", "(a, b)")

def test_parse_test_expr_list():
    parse_test("ExprList", "(1, 1, 1)")    


    
# ------------------------------------------------------------------    
def test_ast_binop_star():
    parse_test("Binop", "*")
def test_ast_binop_plus():
    parse_test("Binop", "+")
def test_ast_binop_fslash():
    parse_test("Binop", "/")   
def test_ast_binop_minux():
    parse_test("Binop", "-")    
def test_ast_binop_left_shift():
    parse_test("Binop", "<<")    
def test_ast_binop_right_shift():
    parse_test("Binop", ">>")
    
def test_stmt_1():
    parse_test("Stmt", "a = 23")
def test_stmt_2():
    parse_test("Stmt", ". = 23")
def test_stmt_3():
    parse_test("Stmt", ". = 23 << 1") 
def test_stmt_4():
    parse_test("Stmt", ". = 1+(-0x23 << --0b01)")
def test_stmt_5():
    parse_test("Stmt", "betaopc(0x1B,RA,0,RC)")   
def test_stmt_6():
    parse_test("Stmts", "a=10 b=20 a b c")
def test_stmt_7():
    parse_test("Stmts", "a=10 \n b=20 \n c=30 \n")
def test_stmt_8():
    parse_test("Stmts", "A")
def test_stmt_9():
    parse_test("Stmts", ". . . .")

    
def test_macro_0():
    parse_test("Macro", ".macro CALL(label) BR(label, LP) //asdf \n")
def test_macro_1():
    parse_test("Macro", ".macro RTN() JMP(LP)\n")
def test_macro_2():
    parse_test("Macro", ".macro XRTN() JMP(XP)\n")
def test_macro_3():
    parse_test("Macro", ".macro GETFRAME(OFFSET, REG) LD(bp, OFFSET, REG) \n")
def test_macro_4():
    parse_test("Macro", ".macro PUTFRAME(REG, OFFSET) ST(REG, OFFSET, bp) \n")
def test_macro_5():
    parse_test("Macro", ".macro CALL(S,N) BR(S,lp) SUBC(sp, 4*N, sp) \n")
def test_macro_6():
    parse_test("Macro", ".macro ALLOCATE(N) ADDC(sp, N*4, sp) \n")
def test_macro_7():
    parse_test("Macro", ".macro DEALLOCATE(N) SUBC(sp, N*4, sp) \n")
def test_macro_8():
    parse_test("Macro", ".macro save_all_regs(WHERE) save_all_regs(WHERE, r31)\n")
def test_macro_9():
    parse_test("Macro", ".macro A(a) {\nA\n}")
def test_macro_10():
    parse_test("Macro", ".macro A(a) {A}")
def test_macro_11():
    parse_test("Macro", ".macro extract_field1 (RA, M, N, RB) {\na = 10\n }")
def test_macro_12():
    parse_test("Macro", ".macro A(a) {\nA\n}")
def test_macro_13():
    parse_test("Macro", ".macro A(a) {A\n A\n A}\n\n")
def test_macro_14():
    parse_test("Macro", ".macro JMP(RA, RC) betaopc(0x1B,RA,0,RC)\n ")
def test_macro_15():
    parse_test("Macro", ".macro LD(RA, CC, RC) betaopc(0x18,RA,CC,RC)\n ")
def test_macro_16():
    parse_test("Macro", ".macro LD(CC, RC) betaopc(0x18,R31,CC,RC)\n ")
def test_macro_17():
    parse_test("Macro", ".macro ST(RC, CC, RA) betaopc(0x19,RA,CC,RC)\n ")
def test_macro_18():
    parse_test("Macro", ".macro ST(RC, CC) betaopc(0x19,R31,CC,RC)\n ")
def test_macro_19():
    parse_test("Macro", ".macro LDR(CC, RC) BETABR(0x1F, R31, RC, CC)\n")
def test_macro_20():
    parse_test("Macro", ".macro PUSH(RA) ADDC(SP,4,SP)  ST(RA,-4,SP)\n ")
def test_macro_21():
    parse_test("Macro", ".macro POP(RA) LD(SP,-4,RA)   ADDC(SP,-4,SP)\n ")

def test_top_level_0():
    parse_test("Macro", ".macro A (RA, M, N, RB) {a = 10}") 
def test_top_level_1():
    parse_test("Macro", ".macro PUTFRAME(REG, OFFSET)  ST(REG, OFFSET, bp)\n") 
def test_top_level_2():
    parse_test("Macro", ".macro PUTFRAME(REG, OFFSET)  ST(REG, OFFSET, bp)\n") 
def test_top_level_3():
    parse_test("TopLevel", ".macro PUTFRAME(REG, OFFSET)  ST(REG, OFFSET, bp)\n")
def test_top_level_4():
    parse_test("TopLevel", ".macro LONG(x) WORD(x) WORD(x >> 16) // asdfasdf \n")
def test_top_level_5():
    file_test("macroblock.uasm")
   
def file_test(f):
    txt = open("./tests/"+f).read()
    parse_test("TopLevel", txt)
    
def test_files_1():
    file_test("macroblock.uasm")    
def test_files_2():
    file_test("beta1.uasm")
def test_files_3():
    file_test("beta.uasm")

def test_processor_0():
    parse_test("Proc", '.text "asdf"') 
def test_processor_1():
    parse_test("Proc", '.options mul')
    
def test_parse_test_assn_1():    
    parse_test("Assn", "a = 23")
def test_parse_test_assn_2():    
    parse_test("Assn", ". = 23")
def test_parse_test_assn_3():    
    parse_test("Assn", ". = 23 << 1") 
def test_parse_test_assn_4():    
    parse_test("Assn", ". = 1+(-0x23 << --0b01)")
def test_parse_test_assn_5():    
    parse_test("Assn", "VEC_RESET = 0")
def test_parse_test_assn_6():    
    parse_test("Assn", "VEC_II = 4")
    
def test_parse_test_call_1():
    parse_test("Call", "Hello(asdf,123)") 
def test_parse_test_call_2():
    parse_test("Call", "A_(1,2,3,4,-0x123)")
def test_parse_test_call_3():
    parse_test("Call", "Asdf()")

def test_parse_test_expr_1():    
    parse_test("Expr2", "1 + 2 + (3)")
def test_parse_test_expr_2():    
    parse_test("Expr2", "(1) + 2 + (3)")
def test_parse_test_expr_3():
    parse_test("Expr2", "(1 + 2)")
def test_parse_test_expr_4():
    parse_test("Expr2", "(1+2+3)")
def test_parse_test_expr_5():
    parse_test("Expr2", "((1)+2+3)")
def test_parse_test_expr_6():
    parse_test("Expr2", "(((1)))")
def test_parse_test_expr_7():
    parse_test("Expr2", "((1+1))")
def test_parse_test_expr_8():
    parse_test("Expr2", "((1+(1+1)))")
def test_parse_test_expr_9():
    parse_test("Expr2", "(1+1+(1+(1+1)))")
def test_parse_test_expr_10():
    parse_test("Expr2", "(((1+((1))+(1+(1+1)))))")
def test_parse_test_expr_11():
    parse_test("Expr2", "1+(2+3)+4")
def test_parse_test_expr_12():
    parse_test("Expr2", "1020 + 0xDeadBeef + 0b101 + (3)")
def test_parse_test_expr_13():
    parse_test("Expr2", "1020 << 0xDeadBeef - (0b101 / (3))")
def test_parse_test_expr_14():
    parse_test("Expr2", "(-1020 + -0x200)") 
def test_parse_test_expr_15():
    parse_test("Expr2", "-(1 + -1)")
def test_parse_test_expr_16():
    parse_test("Expr2", "--(1 + -1)")
def test_parse_test_expr_17():
    parse_test("Expr2", "--(---1 + --(--1))")
def test_parse_test_expr_18():
    parse_test("Expr2", "--(--1%--(2>>1--1))")
def test_parse_test_expr_19():
    parse_test("Expr2", "(.+_-_+.)")
def test_parse_test_expr_20():
    parse_test("Expr2", "-(.)+.+-.")


