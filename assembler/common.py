# -*- coding: utf-8 -*-

DEBUG = False

class Epsilon(object):
    def eval(self):
        return None
    def is_seq(self):
        return False
    def augment_symbol_table(self, st):
        return st 
    def replace_idents(self, st):
        pass
    def generate(self, _):
        return []
    def pretty(self, depth):
        return " "*depth + str(self)
    def __repr__(self):
        return "ε"

def is_epsilon(x):
    if x.__class__.__name__ == "Epsilon":
        return True
    if type(x) == list:
        return False
    if type(x) == str:
        return False
    if x.__class__.__name__ == "Token":
        return False
    if x == None:
        return False
            
    return x.is_epsilon()
    
def epsilon():
    return True, Epsilon()

no_match = False, None

