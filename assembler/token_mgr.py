#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
import inspect
from util import Seq
import util
from common import (no_match, is_epsilon)
import common

class TokenMgr(object):
    def __init__(self, tokens):
        self.tokens = tuple(tokens)
        self.tok_idx = 0
        self.stack = []

        
    def tokens_depleted(self):
        return self.tok_idx == len(self.tokens)

    def remaining(self):
        return self.tokens[self.tok_idx:]
    
    def next_token(self, tok):
        '''grab the next token'''
        if self.tokens_depleted():
            return False, None
        if self.tokens[self.tok_idx].kind == tok:
            x = True, self.tokens[self.tok_idx]
            self.tok_idx += 1
            return x
        return False, None
    
    def restore(self, n):
        '''rewind token index in case where parser rule fails'''
        self.tok_idx -= n
        assert self.tok_idx >= 0
        
    def sequence(self, parse_method, *args):
        '''seq is a method which consumes sequences of tokens.
        '''
        acc = Seq()
        acc.set_parse_method(parse_method)

        tokensConsumed = 0             
        for p in args:
            ignoreFlag = False
            
            if type(p) == str:
                ignoreFlag, p = util.deflag(p)
                b, r = self.next_token(p)
            elif inspect.isfunction(p):
                b, r = p()
            else:
                print "got type: ", type(p)
                raise Exception("Got neither String nor Rule")
            if not is_epsilon(r) and not ignoreFlag:
                acc.append(r)
            if not b:
                self.restore(tokensConsumed)
                return no_match
            tokensConsumed += 1
        return True, util.reduce_seq(acc)
    
    def choice(self, *args):
        "choice rule constructor"
        if common.DEBUG: print self.tokens
        act, args = args[0], args[1:]

        for p in args:
            if type(p) == str:
                b, r = self.next_token(p)
            elif inspect.isfunction(p):
                b, r = p()
            else: 
                print "got type: ", type(p)
                raise Exception("Got neither String nor Rule")
            if b:
                return b, act(r)
        return False, None

