# TODO: add source information

from .encoder import Register, OperandType

class AstNode:
    def __init__(self, parent: "AstNode | None" = None, children: list["AstNode"] = []):
        self.parent = parent
        self.children = children

    def __getitem__(self, key):
        return self.children[key]

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        return f"\"AstNode\": {{ \"children\": {self.children} }}"

    def append(self, child: "AstNode | None" = None):
        if child is None:
            raise ValueError("can't append None to ast node")

        child.parent = self
        self.children.append(child)
        return child

    def encode(self, output: bytes):
        for child in self.children:
            child.encode(output)


# a node that can't have children
class LeafNode(AstNode):
    def __init__(self, parent: "AstNode | None" = None):
        self.parent = parent
        self.children = []

    def __getitem__(self, key):
        return NotImplemented

    def __len__(self):
        return 0

    def __repr__(self):
        return "LeafNode"

    def append(self, child: "AstNode"):
        pass

    def encode(self, output: bytes):
        pass


class LabelNode(AstNode):
    def __init__(self, name: str, parent: "AstNode | None" = None, children: list["AstNode"] = []):
        self.name = name
        self.parent = parent
        self.children = children
        self.offset = 0

    def __repr__(self):
        return f"\"LabelNode\": {{ \"name\": \"{self.name}\", \"children\": {self.children} }}"

    def encode(self, output: bytes):
        self.offset = len(output)


class InstructionNode(AstNode):
    def __init__(self, mnemonic: str, parent: "AstNode | None" = None, operands: list["AstNode"] = []):
        self.mnemonic = mnemonic
        self.parent = parent
        self.children = operands

    def __repr__(self):
        return f"\"InstructionNode\": {{ \"mnemonic\": \"{self.mnemonic}\", \"operands\": {self.children} }}"

    def encode(self, output: bytes):
        # TODO: pick the right encoding
        return NotImplemented


class PointerNode(AstNode):
    # children are registers or a string referring to a label
    def __init__(self, parent: "InstructionNode", type: OperandType, base: "RegisterNode | str", offset: int = 0):
        self.parent = parent
        self.type = type
        self.base = base
        self.offset = 0

    def __repr__(self):
        return f"\"PointerNode\": {{ \"type\": \"{self.type}\", \"base\": \"{self.base}\", \"offset\": {self.offset} }}"

    def encode(self, output: bytes):
        # TODO: figure out how to encode this
        return NotImplemented


class RegisterNode(LeafNode):
    def __init__(self, register: Register, parent: "InstructionNode | PointerNode | None" = None):
        self.register = register
        self.parent = parent

    def __repr__(self):
        return f"\"RegisterNode\": {{ \"register\": \"{self.register}\" }}"

    def encode(self, output: bytes):
        # TODO: figure this out
        return NotImplemented
