import sys
sys.path.append("../")

from lexer import lexer
import parse
import ast    
    
def eval_lambda(rule, text, testFunc):
    p = parse.build_parser(lexer.lex_string(text))
    result = p.parse(rule, text)

    r = result.eval()
    if testFunc(r):
        pass
    else:
        print "--------------------------------------------"
        print "               rule: %s" % rule
        print "               text: %s" % text
        print "                got: %s" % r
        print ('r', r, type(r))
        assert testFunc(r)
            
def test_eval_lit_num_dec():
    eval_lambda("LitNum", "42", lambda x: x.eval() == ast.Number(42))
    
def test_eval_lit_num_hex():
    eval_lambda("LitNum", "0x2a", lambda x: x.eval() == ast.Number(42))
    
def test_eval_lit_num_bin():
    eval_lambda("LitNum", "0b101010", lambda x: x.eval() == ast.Number(42))
            
def test_ast_ident_eval():
    eval_lambda("Ident", "asdf", lambda x: x.__class__.__name__ == "Ident")
    eval_lambda("Ident", "asdf", lambda x: str(x) == "<Ident asdf>")

def test_term_token():
    eval_lambda("Term", "asdf", lambda x: x.parse_obj.tok == "asdf")

def test_term_hex():    
    eval_lambda("Term", "0x10", lambda x: x.eval() == ast.Number(0x10))

def test_term_decimal():    
    eval_lambda("Term", "1", lambda x: x.eval() == ast.Number(1))

def test_term_binary_lit_0():
    eval_lambda("Term", "0b101", lambda x: x.eval() == ast.Number(0b101))
    
def test_term_binary_lit_1():
    eval_lambda("Term", "-0b101", lambda x: x.eval() == ast.Number(-0b101))
    
def test_term_negative_term():    
    eval_lambda("Term", "-1", lambda x: x.eval() == ast.Number(-1))
    
def test_term_neg_neg_term():    
    eval_lambda("Term", "--1", lambda x: x.eval() == ast.Number(1))

# ------------------------------------------------------------------    
def test_expr2_negative_term_0():    
    eval_lambda("Expr2", "-1", lambda x: x.eval() == ast.Number(-1))
    
def test_expr2_negative_term_paren_1():    
    eval_lambda("Expr2", "(-1)", lambda x: x.eval() == ast.Number(-1))
    
def test_expr2_negative_term_paren_2():    
    eval_lambda("Expr2", "((((((((-1))))))))", lambda x: x.eval() == ast.Number(-1))
    
def test_expr2_parens_binop_0():    
    eval_lambda("Expr2", "(1 + 2 + 3)", lambda x: x.eval() == ast.Number(6))

def test_expr2_parens_binop_1():    
    eval_lambda("Expr2", "(1 + (2 + 3))", lambda x: x.eval() == ast.Number(6))

def test_expr2_parens_binop_2():    
    eval_lambda("Expr2", "((1 + 1) + (1 + 1))", lambda x: x.eval() == ast.Number(4))
    
def test_expr2_parens_binop_3():    
    eval_lambda("Expr2", "1 + 2", lambda x: x.eval() == ast.Number(3))

def test_expr2_parens_binop_4():    
    eval_lambda("Expr2", "2 - 1", lambda x: x.eval() == ast.Number(1))
    
def test_expr2_parens_binop_5():    
    eval_lambda("Expr2", "(5 - (3 - 1))", lambda x: x.eval() == ast.Number(3))

def test_expr2_parens_binop_6():    
    eval_lambda("Expr2", "23 - 5 - 2", lambda x: x.eval() == ast.Number(16))
    
def test_expr2_parens_binop_7():    
    eval_lambda("Expr2", "1+2+3+4+5", lambda x: x.eval() == ast.Number(15))
    
def test_expr2_parens_binop_8():    
    eval_lambda("Expr2", "(1+2)+3+4+5", lambda x: x.eval() == ast.Number(15))
    
def test_expr2_parens_binop_9():    
    eval_lambda("Expr2", "((1+2)+3)+4+5", lambda x: x.eval() == ast.Number(15))

def test_expr2_parens_binop_10():    
    eval_lambda("Expr2", "(((1+2)+3)+(4+5))", lambda x: x.eval() == ast.Number(15))

def test_expr2_parens_binop_11():    
    eval_lambda("Expr2", "-(((1+2)+3)+(4+5))", lambda x: x.eval() == ast.Number(-15))

def test_expr2_parens_binop_12():    
    eval_lambda("Expr2", "-(((1+2)+3+3)-(4+5))", lambda x: x.eval() == ast.Number(0))

# ------------------------------------------------------------------
# rooting out negative kerfuffle.

def test_expr2_negs_0():    
    eval_lambda("Expr2", "-1", lambda x: x.eval() == ast.Number(-1))

def test_expr2_negs_1():    
    eval_lambda("Expr2", "(-1)+1", lambda x: x.eval() == ast.Number(0))

def test_expr2_negs_2():    
    eval_lambda("Expr2", "(-1)+(-1)", lambda x: x.eval() == ast.Number(-2))
    
def test_expr2_negs_3():    
    eval_lambda("Expr2", "-((-1)+(-1))", lambda x: x.eval() == ast.Number(2))

def test_expr2_negs_4():    
    eval_lambda("Expr2", "-(-1)", lambda x: x.eval() == ast.Number(1))
    
def test_expr2_negs_4_1():    
    eval_lambda("Expr2", "-(2 - 3)", lambda x: x.eval() == ast.Number(1))
    
def test_expr2_negs_5():    
    eval_lambda("Expr2", "-1 + 1", lambda x: x.eval() == ast.Number(0))
    
def test_expr2_negs_6():    
    eval_lambda("Expr2", "-(1 + 1)", lambda x: x.eval() == ast.Number(-2))
    
def test_expr2_negs_7():    
    eval_lambda("Expr2", "-(-2) - 3", lambda x: x.eval() == ast.Number(-1))

def test_expr2_negs_8():    
    eval_lambda("Expr2", "1 - 1 - 1", lambda x: x.eval() == ast.Number(-1))

def test_expr2_negs_9():    
    eval_lambda("Expr2", "-1 - -1", lambda x: x.eval() == ast.Number(0))

def test_expr2_negs_10():    
    eval_lambda("Expr2", "(-1) + -(1)", lambda x: x.eval() == ast.Number(-2))

def test_expr2_negs_11():    
    eval_lambda("Expr2", "-(-(1) - -1)", lambda x: x.eval() == ast.Number(0))

def test_expr2_negs_12():    
    eval_lambda("Expr2", "--2", lambda x: x.eval() == ast.Number(2))
    
def test_expr2_negs_13():    
    eval_lambda("Expr2", "---2", lambda x: x.eval() == ast.Number(-2))
    
def test_expr2_negs_14():    
    eval_lambda("Expr2", "----2", lambda x: x.eval() == ast.Number(2))

def test_expr2_negs_15():    
    eval_lambda("Expr2", "--(2+2)", lambda x: x.eval() == ast.Number(4))

def test_expr2_negs_16():    
    eval_lambda("Expr2", "----2 + ----2", lambda x: x.eval() == ast.Number(4))

def test_expr2_negs_17():    
    eval_lambda("Expr2", "---(((1+2)+3+3)-(4+6))",
                lambda x: x.eval() == ast.Number(1))

def test_expr2_negs_18():    
    eval_lambda("Expr2", "1--2", lambda x: x.eval() == ast.Number(3))

def test_expr2_negs_19():    
    eval_lambda("Expr2", "1+-2", lambda x: x.eval() == ast.Number(-1))

def do_test_expr2_with_args(s, n):    
    eval_lambda("Expr2", s, lambda x: x.eval() == ast.Number(n))

def test_expr2_torture():
    ''' generate binary expressions and test them'''
    import random
    def genNum():
        return random.randrange(-500000, 500000)
    
    def maybeNegate(x):
        return random.choice([str(x), "-"+str(x)])

    def maybeParen(x):
        return random.choice([str(x), "(" + str(x) + ")"])
    
    def genExpr(n):
        if n == 0:
            return maybeNegate(maybeParen(maybeNegate(genNum())))
        if random.random() > .5:
            op = random.choice("+-")
            return maybeParen(maybeNegate(genExpr(n-1)) + op +
                              maybeNegate(genExpr(n-1)))
        else:
            return maybeNegate(genExpr(n-1))
        
    NUM_TRIALS = 20
    RECURSIONS = 10
    for i in range(NUM_TRIALS):
        s = genExpr(RECURSIONS)
        do_test_expr2_with_args(s, eval(s))

def eval_expr2(s):
    eval_lambda("Expr2", s, lambda x: x.eval() == ast.Number(eval(s)))
def eval_expr2_expect(s, e):
    eval_lambda("Expr2", s, lambda x: x.eval() == ast.Number(e))
    
        
def test_expr2_mul_1(): eval_expr2("1*2")
def test_expr2_mul_2(): eval_expr2("2*3")
def test_expr2_mul_3(): eval_expr2("2*3+2")
def test_expr2_mul_4(): eval_expr2_expect("1*2+3*4", 20)
def test_expr2_mul_5(): eval_expr2("2*3*(5+7)")

#------------------------------------------------------------------    
def test_expr2_mod_1(): eval_expr2("1%2%3%4")
def test_expr2_mod_2(): eval_expr2_expect("4%3*1%2", 4%(3*(1%2)))
def test_expr2_mod_3(): eval_expr2_expect("4%3*1/1", 4%(3*(1/1)))

def test_expr2_mod_4(): eval_expr2_expect("0%256", 0%256)
def test_expr2_mod_5(): eval_expr2_expect("1%256", 1%256)


# ------------------------------------------------------------------
def test_expr2_div_1(): eval_expr2("1/2")
def test_expr2_div_2(): eval_expr2("123/(5/3)")
def test_expr2_div_3(): eval_expr2("8/4/2")
def test_expr2_div_4(): eval_expr2("123/7/3/1")
def test_expr2_div_5(): eval_expr2("(1*(2+(4/3)))<<4")
def test_expr2_div_6(): eval_expr2("(1<<(2+(4/3)))<<4")
def test_expr2_div_7(): eval_expr2("1/1/1/1/1/1/1/1")

# ==================================================================
def test_expr2_shift_1(): eval_expr2("1<<1")
def test_expr2_shift_2(): eval_expr2("2<<1")
def test_expr2_shift_3(): eval_expr2("4<<2")
def test_expr2_shift_4(): eval_expr2("-(4/2)<<2")
def test_expr2_shift_5(): eval_expr2("(-4/2)<<2")

# ==================================================================
def test_expr2_beef_shift_0(): eval_expr2("2 >> 2")
def test_expr2_beef_shift_1(): eval_expr2("0xdeadbeef >> 8")
def test_expr2_beef_shift_2(): eval_expr2("(0xdeadbeef >> 8) % 0x100")


# evaluating with symbols.
