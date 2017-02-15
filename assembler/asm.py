import sys
sys.path.append("../")

import gen
import util
import ast
from symbol_table import SymbolTable


class Assembler(object):
    def __init__(self, src, include_dirs=()):
        self.gen = gen.Generation(src)
        self.cur_byte = 0
        self.symtab = SymbolTable()
        self.pass1 = []
        self.asm_inst = []
        
        self.symtab = self.gen.symbol_pass(self.symtab)
        # numNames = self.symtab.num_symbols()
        # guard = 0
        
        # while True:
        #     # set a limit to how many passes, just in case.
        #     guard += 1
        #     if guard > 1:
        #         break #util.die("having issues resolving symbols")
            
        #     self.gen.replace_idents(self.symtab)
        #     symtab = self.gen.symbol_pass(self.symtab)
        #     if symtab.num_symbols() == numNames:
        #         break
            
        self.asm_inst = self.gen.generate(self.symtab)
        
    def inc(self):
        self.cur_byte += 1
        
    def emit(self, n):
        # if n != 0xff & n:
        #     util.die("Can't emit a value larger than 255")
        # self.out.append((self.cur_byte, n & 0xff))
        self.pass1.append(n)
        self.inc()
        
    def emit_until(self, x, n):
        while self.cur_byte < n:
            self.emit(ast.Number(x))
            
    def process_asm_inst(self):
        for inst in self.asm_inst:
            # check to see if inst an assembly instruction, or
            # something waiting to be eval'd
            self.symtab.insert(".", ast.Number(self.cur_byte))
            
            if not inst.is_assembler_inst():
                # This is a mess, it seems like there oughta be two passes.
                inst.replace_idents(self.symtab)
                val = inst.eval()
                self.emit(val)
                
            elif inst.name == "LABEL":
                print inst, self.cur_byte
                self.symtab.insert(inst.val, ast.Number(self.cur_byte))
                
            elif inst.name == "NUMBER":
                self.emit(inst.val)
                
            elif inst.name == "DOT_ALIGN":
                alignTo = inst.val.val
                if self.cur_byte % alignTo != 0:
                    addr = (self.cur_byte/alignTo) * alignTo + alignTo
                    self.emit_until(0, addr)

            elif inst.name == "DOT":
                self.emit(ast.Number(self.cur_byte))

                    
            elif inst.name == "ASSN":
                ident = inst.val[0]
                expr = inst.val[1]
                expr.replace_idents(self.symtab)
                self.symtab.insert(ident.name(), expr.eval())
                
            elif inst.name == "DOT_ASSN":
                tgt = inst.val(ast.Number(self.cur_byte))
                tgt.replace_idents(self.symtab)
                n = tgt.eval().val
                if n < self.cur_byte:
                    raise Exception("Can't set (.) address backwards")
                # emit a bunch of zeros until reached the tgt addr.
                self.emit_until(0, n)
            else:
                util.die("Encountered unknown assembler instruction: " + inst.name)
        return self.pass2()
    
    def pass2(self):
        temp = []
        for expr in self.pass1:
            expr.augment_symbol_table(self.symtab)
            expr.replace_idents(self.symtab)
            temp.append(expr.eval().val)
        return zip(xrange(0,int(1e9)), temp)
