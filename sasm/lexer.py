# fairly simple, assembly is nice like that

import re

from .ast import AstNode, LabelNode, PointerNode, InstructionNode, RegisterNode
from .desc import Desc
from .encoder import OperandType

COMMENT_CHAR = ';'
LABEL_CHAR = ':'
POINTER_KEYWORD = "PTR"
OPERAND_SEPARATOR = ','


def has_no_whitespace(x: str) -> bool:
    return len(list(filter(lambda x: x.isspace(), x))) == 0


def lex_label(parent: AstNode | None, line: str):
    # always ends with a colon, get rid of that
    line = line[:-1].strip()
    if has_no_whitespace(line):
        return LabelNode(line, parent)

    raise SyntaxError(f"invalid label {line}")


def lex_pointer(desc: Desc, parent: InstructionNode, line: str):
    # pointers start with a size and the word "ptr"
    sizes = {
        "BYTE": OperandType.M8,
        "WORD": OperandType.M16,
        "DWORD": OperandType.M32
    }
    parts = line.split()
    if len(parts) > 2 and parts[0].upper() in sizes.keys() and parts[1].upper() == POINTER_KEYWORD:
        ptr = "".join(parts[2:]) # reassemble later parts to a string
        addr = re.match("[(\\S+)]", ptr) # third piece of "line" is the part in brackets
        if addr is None:
            raise SyntaxError(f"bad pointer expression {addr}")
        addr = addr[0].strip()

        # TODO: parse address

        return PointerNode(parent, sizes[parts[0]], "")

    raise SyntaxError(f"invalid pointer {line}")


def lex_instruction(desc: Desc, parent: AstNode | None, line: str):
    parts = line.split() # split the line
    mnemonic = parts[0] # get the mnemonic
    node = InstructionNode(mnemonic, parent)
    if len(parts) > 1: # if there are operands, parse them
        # just lazily split by commas
        operands = [operand.strip() for operand in line[len(mnemonic):].split(OPERAND_SEPARATOR)]
        for operand in operands:
            if operand in desc.registers.keys():
                node.append(RegisterNode(desc.registers[operand]))
            else: # can only be a pointer
                node.append(lex_pointer(desc, node, operand))

    return node


def lex(desc: Desc, source: str) -> AstNode:
    lines = source.splitlines()
    root = AstNode()

    cur: AstNode = root
    for line in lines:
        line = line.split(COMMENT_CHAR)[0].strip()
        if len(line):
            # things can be a comment, a label, or an instruction
            if line[0] == COMMENT_CHAR:
                pass
            # when you have a label, it becomes the current parent
            #
            # "local" labels that you can do in some assemblers (like ".something" would turn into "global_label.something" in nasm)
            # aren't implemented
            elif line[-1] == LABEL_CHAR:
                cur = root.append(lex_label(cur, line))
            # there's no sections or related directives (that's not necessary for flat binary tbh), and no directives for emitting bytes like "dw 0xaa55".
            # maybe emitting bytes would make this actually functional but it's just a proof of concept really so i won't prioritize it
            else:
                cur.append(lex_instruction(desc, cur, line))

    print(root)
    return root
