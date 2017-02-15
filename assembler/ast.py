import common
import util
import macro
import symbol_table

# ------------------------------------------------------------------            
class Node(object):
    def __init__(self, parse_obj):
        '''the parser applies Node constructors as actions while parsing
        '''
        self.parse_obj = parse_obj
    def is_seq(self):
        return util.type_is(self.parse_obj, "Seq")
    def __repr__(self):
        return "(Node:%s %s)" % (self.__class__.__name__,
                                 self.parse_obj)
    def is_epsilon(self):
        return common.is_epsilon(self.parse_obj)
    
    def replace_idents(self, symtab):
        if self.parse_obj.is_seq():
            for obj in self.parse_obj:
                obj.replace_idents(symtab)                
        else:
            self.parse_obj.replace_idents(symtab)

    def eval(self):
        return self

    def is_assembler_inst(self): return False
    
    def unbound(self):
        if self.parse_obj.is_seq():
            temp = False
            for obj in self.parse_obj:
                temp = temp or obj.unbound()
            return temp
        else:
            return self.parse_obj.unbound()
    
    def generate(self, symtab):
        if self.parse_obj.is_seq():
            result = []
            for obj in self.parse_obj:
                result += obj.generate(symtab)
            return result 
        else:
            return self.parse_obj.generate(symtab)
    
    def __len__(self):
        if self.is_seq():
            return len(self.parse_obj)
        return 1
    
    def augment_symbol_table(self, symtab):
        if self.parse_obj.is_seq():
            for obj in self.parse_obj:
                symtab = obj.augment_symbol_table(symtab)
        else:
            symtab = self.parse_obj.augment_symbol_table(symtab)
        return symtab
            
    def parse_method(self):
        if self.is_seq():
            return self.parse_obj.parse_method
        return None
    def __getitem__(self, n):
        if self.is_seq():
            return self.parse_obj[n]
        raise Exception("This node's parse object is not a sequence")
    def pretty(self, depth=0):
        if self.is_seq():
            print "::" + " " * depth, self.__class__.__name__
            for item in self.parse_obj:
                item.pretty(depth+1)
        else:
            self.parse_obj.pretty(depth+1)

# ------------------------------------------------------------------            
class Binop(Node):
    def is_negative(self):
        return self.parse_obj.kind == "SUB"
    def __repr__(self):
        return "<Binop `%s`>" % self.parse_obj

# ------------------------------------------------------------------            
class Number(object):    
    def __init__(self, n):
        self.val = n
        if util.is_number(n):
            self.val = n.val
    def __neg__(self):
        return Number(-self.val)
    def eval(self):
        return self
    def __add__(self, other):
        return Number(self.val + other.val)
    def __sub__(self, other):
        return Number(self.val - other.val)
    def __mul__(self, other):
        return Number(self.val * other.val)
    def __mod__(self, other):
        return Number(self.val % other.val)
    def __div__(self, other):
        return Number(self.val / other.val)
    def __lshift__(self, other):
        return Number((self.val << other.val))
    def __rshift__(self, other):
        return Number((self.val >> other.val))
    def generate(self, _):
        return [AssemblerInst("NUMBER", self)]
    def __repr__(self):
        return "<Number %d>" % self.val
    def pretty(self, depth):
        return " "*4 + str(self)
    def replace_idents(self, _): pass    
    def augment_symbol_table(self, st):
        return st
    def is_seq(self):
        return False
    def __eq__(self, other):
        if util.same_type(self, other):
            return self.val == other.val
        return False
    
# ------------------------------------------------------------------            
class LitNum(Node):
    def eval(self):
        base = 10
        if self.parse_obj.kind == "HEXNUM": base = 16
        elif self.parse_obj.kind == "BINNUM": base = 2
        val = int(self.parse_obj.tok, base)
        return Number(val)
    
    def __repr__(self):
        return "<LitNum %s>" % self.eval()

# -------------------------------------------------------------------
class QuotedPath(Node): pass

# ------------------------------------------------------------------            
class Ident(Node):
    def __init__(self, *args):
        Node.__init__(self, *args)
        self.value = None
        
    def augment_symbol_table(self, symtab):
        if self.value != None:
            symtab.insert(self.name(), self.value)
        return symtab
    
    def name(self):
        return self.parse_obj.tok
    def __eq__(self, other):
        if util.same_type(self, other):
            return self.name() == other.name()
        return False
    
    def replace_idents(self, symtab):
        if self.name() in symtab:
            self.value = symtab.lookup(self.name())

    def eval(self):
        if self.value:
            return self.value
        return self
    
    def unbound(self): return True
    def __neq__(self, other): return not (self == other)
    def __repr__(self):
        return "<Ident %s>" % self.parse_obj
    
# ------------------------------------------------------------------            
class Term(Node):
    def negate(self):
        return -self.eval()
    
    def eval(self):
        if self.is_seq():
            if self.parse_method() == "eval1":
                # lambda: seq("eval1", "SUB", Term),
                return -self[1].eval()
            
            if self.parse_method() == "eval2":
                # lambda: seq("eval2", "~LPAREN", Expr2, "~RPAREN"),
                return self[0].eval()
        else:
            return self.parse_obj.eval()        
    def __repr__(self):        
        return "<Term %s>" % self.parse_obj
    
# ------------------------------------------------------------------            
class Expr2(Node):
    '''
    def Expr2(): return cho(
            ast.Expr2,
            lambda: seq("eval1", "SUB", Expr2), 
            lambda: seq("eval2", Term, Expr1),
            lambda: seq("eval2", "~LPAREN", Term, Expr1, "~RPAREN"),
    )
    '''
    def negate_first(self):
        ''' negate the first parse object '''
        self.parse_obj[0] = self[0].negate()
        return self
    
    def eval(self):        
        if self.parse_method() == "eval1":
            # seq("eval1", "SUB", Expr2),
            assert self[0].tok == "-"
            assert util.type_is(self[1], "Expr2")

            expr2 = self[1]
            # check to see if the first parse object is a negative
            # sign, i.e. check for double negative.
            if util.type_is(expr2[0], "Token"):
                if expr2[0].kind == "SUB":
                    return expr2[1].eval()
                            
            return expr2.negate_first().eval()
        
        elif self.parse_method() == "eval2": 
            # seq("eval2", Term, Expr1),
            term = self[0]

            # maybe Expr1 was epsilon.
            if len(self) == 1: return term.eval()
            
            expr1 = self[1]
            def subEval(term, expr1):
                t = term.eval()
                e = expr1.eval()
                
                if len(e) == 3:
                    if util.type_is(e[2], "Seq"):
                        op = e[0]
                        lhs = t.eval()
                        eb = ExprBin(op, lhs, e[1])
                        return subEval(eb.eval(), e[2].eval())
                    else:
                        util.deadcode()
                elif len(e) == 2:
                    return ExprBin(e[0].eval(), t, e[1].eval())
                else:
                    util.deadcode()
                    
            return subEval(term, expr1).eval()
        else:
            util.deadcode()

    def generate(self, symtab):
        # import pdb; pdb.set_trace()
        return self.eval().generate(symtab)
            
    def __repr__(self):
        return "<Expr2 %s>" % self.parse_obj
    
def maybeEval(x):
    if x == None:
        return None
    return x.eval()

# ------------------------------------------------------------------            
class ExprBin(object):
    def __init__(self, op, term, expr1):
        self.op = op
        self.left = maybeEval(term)
        self.right = maybeEval(expr1)
        
    def ready(self):
        if self.left == None or self.right == None:
            return False
        if not util.is_number(self.left.eval()):
            return False
        if not util.is_number(self.right.eval()):
            return False
        return True

    def is_assembler_inst(self): return False
    def augment_symbol_table(self, _): return
    
    def replace_idents(self, symtab):
        if self.left != None:
            self.left.replace_idents(symtab)               
        if self.right != None:
            self.right.replace_idents(symtab)
    
    def pretty(self, depth):
        self.op.pretty(depth)
        if self.left != None: self.left.pretty(depth+1)
        if self.right != None: self.right.pretty(depth+1)

    def is_seq(self): return False
        
    def eval(self):
        if self.ready():
            op = {
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y,
                "*": lambda x, y: x * y,
                "/": lambda x, y: x / y,
                "%": lambda x, y: x % y,
                "<<": lambda x, y: x << y,
                ">>": lambda x, y: x >> y,
              }[self.op.parse_obj.tok]
            # both sides have args, so eval them.
            # print self.left, self.right
            return op(self.left.eval(), self.right.eval())
        else:
            return self

    def generate(self, symtab):
        if self.ready():
            return self.eval().generate(symtab)
        else:
            return [self]
        
    def __repr__(self):
        return "(ExprBin <%s %s %s>)" % (self.left, self.op, self.right)
    
# ------------------------------------------------------------------            
class Expr1(Node):
    '''
    def Expr1(): return cho (
            ast.Expr1,
            lambda: seq("eval1", Binop, Term, Expr1),
    )
    '''    
    def eval(self):
        if self.is_seq():
            # lambda: seq("eval1", Binop, Term, Expr1),
            if self.parse_method() == "eval1":
                numObj = len(self.parse_obj)
                assert numObj in [2,3]                
                if numObj == 2:
                    # Since only two objects, Expr1 was an epsilon.
                    binop = self[0]
                    term = self[1]
                    assert util.type_is(binop, "Binop")
                    assert util.type_is(term, "Term")
                    return util.Seq(binop, term.eval())
                
                elif numObj == 3:
                    binop = self[0]
                    term = self[1]
                    expr = self[2]
                    assert util.type_is(binop, "Binop")
                    assert util.type_is(term, "Term")
                    assert util.type_is(expr, "Expr1")
                    
                    return util.Seq(binop, term.eval(), expr.eval())
                else:
                    util.deadcode()
            else:
                util.deadcode()
        else:
            return self.parse_obj.eval()
        
    def __repr__(self):
        return "<Expr1 %s>" % self.parse_obj
    
# ------------------------------------------------------------------            
class RuleSepComma(Node): pass    
class Parened(Node): pass
class IdentSepComma(Node): pass
class IdentList(Node):
    def unnest(self): return util.unnest(self.parse_obj)
    
class ExprSepComma(Node): pass
class ExprList(Node): 
    def unnest(self): return util.unnest(self.parse_obj)
    
class Assn(Node):
    def generate(self, _):
        lhs = self[0]
        if lhs.name() == ".":
            '''HEY! This is a little complicated.  DOT can appear in the
            expression on the RHS and it's up to the assembler to
            evaluate the expression with a dynamic value of DOT.
            So. Need to pass in a function here to delay the eval
            until runtime.

            '''
            def delayEval(curAddr):
                symtab = symbol_table.SymbolTable()
                symtab.insert(".", curAddr)
                self[1].replace_idents(symtab)
                return self[1].eval()
            ai = AssemblerInst("DOT_ASSN", delayEval)
            return [ai]
        
        ai = AssemblerInst("ASSN", self)
        return [ai]
    
    def augment_symbol_table(self, st):
        sym = self[0].name()
        self[1].replace_idents(st)
        val = self[1].eval()
        if util.is_number(val):
            st.insert(sym, val)
            return st
        else:
            return self[1].augment_symbol_table(st)
        
class Call(Node):
    def generate(self, symtab):
        name = self.parse_obj[0].name()
        num_args = len(self.parse_obj[1].unnest())
        mac = symtab.lookup_macro(name, num_args)
        if mac == None:
            msg = "Macro not found: %s"
            raise Exception(msg % name)
        exprList = self.parse_obj[1]
        mac.bind(exprList.unnest())
        return mac.generate(symtab)
    
class Stmt(Node): pass

class Stmt0(Node): 
    # this should not be this way. there is underlying bug here.
    # this method should not be needed.
    def generate(self, s):
        # import pdb; pdb.set_trace()
        # if util.is_ident(self.parse_obj.eval()):
        #     if self.parse_obj.eval().name() == ".":
        #         return [AssemblerInst("DOT", None)]
        return self.parse_obj.generate(s)

    def replace_idents(self, symtab):
        self.parse_obj.replace_idents(symtab)
    
    def augment_symbol_table(self, st):
        return self.parse_obj.augment_symbol_table(st)
    
class SpacedIdents(Node):pass

class AssemblerInst(object):
    def __init__(self, name, expr):
        self.name = name
        self.val = expr

    def is_assembler_inst(self): return True
        
    def __neq__(self, other):
        return not self == other
    
    def __eq__(self, other):
        if not util.type_is(other, "AssemblerInst"):
            return False
        return (self.name == other.name and
                self.val == other.val)
    
    def __repr__(self):
        return "<AssemblerInst name:%s, expr:%s>" % (self.name,
                                                     self.val)
    
class Proc(Node):
    def generate(self, _):
        method, x = self.parse_method(), None
        
        if method == "align":
            name, x = "DOT_ALIGN", self.parse_obj[1].eval()
        elif method == "ascii":
            name, x = "DOT_ASCII", self.parse_obj[1]
        elif method == "text":
            name, x = "DOT_TEXT", self.parse_obj[1]
        elif method == "breakpoint":
            name = "DOT_BREAKPOINT"
        elif method == "protect":
            name = "DOT_PROTECT"
        elif method == "unprotect":
            name = "DOT_UNPROTECT"
        elif method == "options":
            # TODO Do a better job of cleaning up the whitespace between these options.
            name, x = "OPTIONS", self.parse_obj[1].split(" ")[1:]
        elif method == "label":
            name, x = "LABEL", self.parse_obj[0].eval().name()            
            # print name, x
            # if x == "start":
            #     import pdb;pdb.set_trace()            
        elif method == "include":
            return []
        
        else:
            util.die("Unknown processor directive found: " + self.parse_method())
        return [AssemblerInst(name, x)]
    
    def eval(self):
        util.die()
    
class Stmts(Node): pass
    
class Macro(Node):
    def __init__(self, *args):
        Node.__init__(self, *args)
        # # lambda: seq("eval1", "~DOT_MACRO", Ident, IdentList, MacroBody),
        self.name = args[0][0]
        self.args = args[0][1].unnest()
        self.body = args[0][2]
    
    def augment_symbol_table(self, symtab):
        me = macro.MacroExec(self.name, self.args, self.body)
        symtab.insert_macro(self.name.name(), me)
        return symtab
    
    def generate(self, symtab):
        return []
    
class MacroBody(Node): pass    
class TopLevel(Node): pass
