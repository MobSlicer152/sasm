from . import lexer

from .desc import Desc

desc = Desc("x86.json")

source = ""
with open("add.asm", "r") as f:
    source = f.read()

lexer.lex(desc, source)
