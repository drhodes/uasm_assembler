#!/usr/bin/env python
import re
import argparse
import sys

class Token(object):
    def __init__(self, kind, tok, line, col):
        self.kind = kind # kind of token
        self.tok = tok # string value of the token
        self.line = line
        self.col = col 

    def __repr__(self):
        #tmp = self.kind, self.tok, self.line, self.col
        #return "(<%s> %s @line:%d col:%d)" % tmp
        return self.tok
    
    def eval(self):
        return self
        
    def length(self):
        return len(self.tok)

    def pretty(self, depth):
        print "::" + " "*depth, self.tok
        
    def is_seq(self): return False    
    def augment_symbol_table(self, x): return x
    def replace_idents(self, _): pass
    def generate(self, _): return []
    
    def __eq__(self, other):
        if other.__class__.__name__ == "Token":
            return self.tok == other.tok
        return False
    
class TokenBuilder(object):
    def __init__(self, name, pat):
        self.name = name
        self.pat = re.compile(pat)

    def look(self, src):
        '''look ahead into the source, return the number of chars were
        matched'''
        m = self.pat.match(src)
        if m == None:
            return 0
        return m.end()

class Lexer(object):
    def __init__(self, filename, pairs):
        self.filename = filename
        self.cur_col = 0
        self.cur_line = 1
        self.text = ""
        self.builders = [TokenBuilder(*p) for p in pairs]
        self.tokens = []
            
    def get_next_token(self):
        maxLen, tok = (0, None)
        for b in self.builders:
            curLen = b.look(self.text)
            if curLen > maxLen:
                maxLen = curLen
                tok = Token(b.name,
                            self.text[:maxLen],
                            self.cur_line,
                            self.cur_col)                
        # If no tokens where consumed then die.
        if maxLen == 0:
            msg = "Lexer can't tokenize: %s, on line: %d"
            raise Exception(msg % (self.text[:20], self.cur_line))

        if tok.kind == "NEWLINE":
            self.cur_line += 1
            self.cur_col = 0

        if tok.kind == "C_COMMENT":
            self.cur_line += tok.tok.count("\n")

        if tok.kind == "CXX_COMMENT":
            self.cur_line += 1

        ignored = ["SPACES", "CXX_COMMENT", "C_COMMENT", "TABS"]
        if not tok.kind in ignored:
            self.tokens.append(tok)
            
        self.text = self.text[maxLen:]

    def scan(self):
        while len(self.text) > 0:
            self.get_next_token()
            
        # hack for line macros.
        inLineMacro = False
        sawLBRACE = False
        for i in range(len(self.tokens)):
            curTok = self.tokens[i]
            # look for a .macro token
            if not inLineMacro:
                if curTok.kind == "DOT_MACRO":
                    inLineMacro = True
                    continue
            if inLineMacro:
                if curTok.kind == "LBRACE": 
                    # if a "{" was seen
                    sawLBRACE = True
                    continue                
            if inLineMacro:
                # look for a newline token
                # if a { token was not seen, then
                if curTok.kind == "NEWLINE" and not sawLBRACE:
                    # clobber the newline token with "LINEMACRO_END"
                    self.tokens[i].kind = "LINE_MACRO_END"
                    sawLBRACE = False
                    inLineMacro = False
                    continue
            if curTok.kind == "NEWLINE":
                sawLBRACE = False
                inLineMacro = False
                    
        self.tokens = [x for x in self.tokens if x.kind != "NEWLINE"]
        # END HACK
        return self.tokens
        
    def lex(self):
        self.text = open(self.filename).read()
        return self.scan()
        
    def lex_string(self, s):
        self.text = s
        return self.scan()

#------------------------------------------------------------------
arg_parser = argparse.ArgumentParser(description='tokenize .uasm file')
arg_parser.add_argument('-i', '--infile', type=str, help='file to parse')
    
optionsRe = ''.join([ ".options ",
                      "(clk|",
                      "noclk|",
                      "div|",
                      "nodiv|",
                      "mul|",                      
                      "nomul|",
                      "kalways|",
                      "nokalways|",
                      "tty|",
                      "notty|",
                      "annotateif|",
                      "noannotate|",
                      "[ \t])*"])
                    
regexPairs = [ ("IDENT", "[a-zA-Z_]+[a-zA-Z0-9]*"),
               ("OPTIONS", optionsRe),
               ("CXX_COMMENT", "//.*?(?=\n)"), # doesn't this eat the new line?
               ("STRING", r'"[^"]*"'),
               ("COLON", ":"),               
               ("DOT", "\."),
               ("MUL", "\*"),
               ("DIV", "/"),
               ("ADD", "\+"),
               ("SUB", "\-"),
               ("MOD", "\%"),
               ("BITWISE_AND", "\&"),
               ("BITWISE_OR", "\|"),
               ("TILDE", "\~"),
               ("EQUALS", "\="),
               ("COMMA", ","),
               ("LPAREN", "\("),
               ("RPAREN", "\)"),
               ("NEWLINE", "\n"),
               ("SPACES", "[ ]+"),
               ("TABS", "[\t]+"),
               ("DECNUM", "[0-9]+"),               
               ("HEXNUM", "0[x|X][0-9a-fA-F]+"),
               ("BINNUM", "0[b|B][0|1]+"),
               ("SHIFT_L", "<<"),
               ("SHIFT_R", ">>"),
               ("LBRACE", "\{"),
               ("RBRACE", "\}"),
               ("BRACKET_L", "\["),
               ("BRACKET_R", "\]"),
               ("DUB_QUOTE", "\""),
               ("QUOTE", "\'"),
               ("DOT_INCLUDE", "\.include"),
               ("DOT_MACRO", "\.macro"),
               ("DOT_ALIGN", "\.align"),
               ("DOT_ASCII", "\.ascii"),
               ("DOT_TEXT", "\.text"),
               ("DOT_BREAKPOINT", "\.breakpoint"),
               ("DOT_PROTECT", "\.protect"),
               ("DOT_UNPROTECT", "\.unprotect"),
               ("PATH", "[A-Za-z0-9_\-/]"),
               # regex for C_COMMENT found here.
               # http://blog.ostermiller.org/find-comment
               ("C_COMMENT", r"/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/"),
]

def main():
    args = arg_parser.parse_args()
    
    if not any(vars(args).values()):
        arg_parser.print_help()
        print "No args supplied"
        sys.exit()
    if args.infile:
        lex = Lexer(args.infile, regexPairs)
        for tok in lex.lex():
            print tok
            
def lex_file(filename):
    lex = Lexer(filename, regexPairs)
    return lex.lex()    

def lex_string(s):
    lex = Lexer("string", regexPairs)
    return lex.lex_string(s)
            
if __name__ == "__main__":
    main()
