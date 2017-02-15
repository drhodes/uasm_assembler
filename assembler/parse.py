#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import ast
from common import epsilon
from token_mgr import TokenMgr
import util


def build_parser(toks):
    tm = TokenMgr(toks)
    # bind these methods to names: seq and cho for brevity in the
    # productions
    seq = tm.sequence
    cho = tm.choice
    p = Parser(tm)

    action = lambda x:x
    # -------------------------------------------------------
    # UASM Grammar here. 

    # Create a parser class add "rule" method to it that attaches each
    # of these productions by decoration, like
    
    # @parser.rule
    # def Production(): return cho ( ... )
    
    @p.rule
    def Expr2(): return cho(
            ast.Expr2,
            lambda: seq("eval1", "SUB", Expr2), 
            lambda: seq("eval2", Term, Expr1),
            lambda: seq("eval2", "~LPAREN", Term, Expr1, "~RPAREN"),
    )
    
    @p.rule
    def Expr1(): return cho (
            ast.Expr1,
            lambda: seq("eval1", Binop, Term, Expr1),
            epsilon,
    )
    
    @p.rule
    def Term(): return cho (
            ast.Term,
            Ident, 
            LitNum,
            lambda: seq("eval1", "SUB", Term),
            lambda: seq("eval2", "~LPAREN", Expr2, "~RPAREN"),
    )
    
    @p.rule
    def RuleSepComma(action, rule): return cho (
            lambda x:x, #ast.RuleSepComma,
            lambda: seq("eval1", rule, lambda:RuleSepComma(action, rule)),
            lambda: seq("eval2", "~COMMA", rule, lambda:RuleSepComma(action, rule)),
            epsilon,
    )
    
    @p.rule
    def Parened(x):
        return lambda: seq("eval1", "~LPAREN", x, "~RPAREN")
    
    @p.rule
    def IdentSepComma():
        return RuleSepComma(action, "IDENT")
    
    @p.rule
    def IdentList(): return cho (
            ast.IdentList,
            Parened(IdentSepComma)
    )
    
    @p.rule
    def ExprSepComma():
        return RuleSepComma(action, Expr2)
    
    @p.rule
    def ExprList(): return cho (
            ast.ExprList,
            Parened(ExprSepComma),
    )
    
    @p.rule
    def Ident(): return cho (
            ast.Ident,
            "IDENT",
            "DOT",
    )
    
    @p.rule
    def LitNum(): return cho (
            ast.LitNum,
            "HEXNUM",
            "BINNUM",
            "DECNUM"
    )
        
    @p.rule
    def Binop(): return cho (
            ast.Binop,
            "MUL",
            "DIV",
            "ADD",
            "SUB",
            "MOD",
            "BITWISE_AND",
            "BITWISE_OR",
            "TILDE",
            "SHIFT_L",
            "SHIFT_R",
    )
    
    @p.rule
    def Assn(): return cho (
            ast.Assn,
            lambda: seq("eval1", Ident, "~EQUALS", Expr2)
    )
    
    @p.rule
    def Call(): return cho (
            ast.Call,
            lambda: seq("eval1", Ident, ExprList),
    )
    
    @p.rule
    def Stmt(): return cho (
            ast.Stmt,
            Stmt0,
    )
    
    @p.rule   
    def Stmt0(): return cho (
            ast.Stmt0,
            Proc,
            Call,
            Assn,
            Expr2,
    )
   
    @p.rule
    def Proc(): return cho (
            ast.Proc,
            lambda: seq("include", "DOT_INCLUDE", "STRING"),

            lambda: seq("align", "DOT_ALIGN", Expr2),
            lambda: seq("ascii", "DOT_ASCII", "STRING"),
            lambda: seq("text", "DOT_TEXT", "STRING"),
            lambda: seq("breakpoint", "DOT_BREAKPOINT"),
            lambda: seq("protect", "DOT_PROTECT"),
            lambda: seq("unprotect", "DOT_UNPROTECT"),
            lambda: seq("options", "OPTIONS"),
            lambda: seq("label", Ident, "~COLON"),
    )
    
    @p.rule
    def Stmts(): return cho (
            ast.Stmts,
            lambda: seq("eval1", Stmt, Stmts),
            lambda: epsilon(),
    )
    
    @p.rule
    def Macro(): return cho (
            ast.Macro,
            lambda: seq("eval1", "~DOT_MACRO", Ident, IdentList, MacroBody), 
    )
    
    @p.rule
    def MacroBody(): return cho (
            ast.MacroBody,
            lambda: seq("eval1", "~LBRACE", Stmts, "~RBRACE"),
            lambda: seq("eval2", Stmts, "~LINE_MACRO_END"),
    )
    
    @p.rule
    def TopLevel(): return cho (
            ast.TopLevel,
            lambda: seq("eval1", Macro, TopLevel),
            lambda: seq("eval2", Stmt, TopLevel),
            epsilon,
    )
    
    return p

class Parser(object):
    def __init__(self, token_mgr):
        self.token_mgr = token_mgr
        self.rules = {}
        
    def rule(self, x):
        self.rules[x.__name__] = x
        return x

    def parse(self, rule, s):
        if not rule in self.rules:
            raise Exception("Couldn't find production: '%s', in parser" % rule)
        ok, result = self.rules[rule]()

        if not self.token_mgr.tokens_depleted():
            print "PARSING FAILS"
            print rule
            print s
            assert False
        if not ok:
            print result, rule
            assert False

        return result

    def parse_top(self):
        tops = util.Seq()

        while not self.token_mgr.tokens_depleted():
            ok, result = self.rules["Macro"]()
            if ok:
                tops.append(result)
                continue
            ok, result = self.rules["Stmt"]()
            if ok:
                tops.append(result)
                continue
            print self.token_mgr.remaining()
            raise Exception("Failed to parse")

        return tops 
