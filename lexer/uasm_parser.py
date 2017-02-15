import pypeg1
import re

def comment():
    return [re.compile(r"//.*"), re.compile("/\*.*?\*/", re.S)]
def ident():
    return re.compile(r"[a-z|A-Z|_]+[a-zA-Z0-9]*")
