class AstNode:
    def __init__(self, parent: "AstNode | None" = None, children: list["AstNode"] = []):
        self.parent = parent
        self.children = children

    def __getitem__(self, key):
        return self.children[key]

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        return f"AstNode {{ children: {self.children} }}"

    def append(self, child: "AstNode"):
        self.children.append(child)

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


class CommentNode(LeafNode):
    def __init__(self, body: str):
        self.body = body
        self.children = []

    def __repr__(self):
        return f"CommentNode {{ body: {self.body} }}"


class LabelNode(AstNode):
    def __init__(self, name: str, parent: "AstNode | None" = None, children: list["AstNode"] = []):
        self.name = name
        self.parent = parent
        self.children = children

    def __repr__(self):
        return f"LabelNode {{ name: {self.name}, children: {self.children} }}"


class InstructionNode(AstNode):
    def __init__(self, mnemonic: str, parent: "AstNode | None" = None, children: list["AstNode"] = []):
        self.mnemonic = mnemonic
        self.parent = parent
        self.children = children

    def __repr__(self):
        return f"InstructionNode {{ mnemonic: {self.mnemonic}, children: {self.children} }}"

    def encode(self, output: bytes):
        # TODO: pick the right encoding
        return NotImplemented
