from enum import Enum
from typing import Final


class Opcode:
    def __init__(
        self,
        primary: int,
        secondary: int | None = None,
        prefix: int | None = None,
        has_0f: bool = False,
    ):
        self.primary: Final = primary
        self.secondary: Final = secondary
        self.prefix: Final = prefix
        self.has_0f: Final = has_0f

    # produces the bytes that this opcode is represented by
    def encode(self, add: int = 0) -> bytes:
        length = 1
        code = (self.primary & 0xFF) + (add & 0xF)
        if self.secondary is not None:
            length += 1
            code |= (self.secondary & 0xFF) << 8
        if self.has_0f:
            length += 1
            code = (code << 8) | 0x0F
        if self.prefix is not None:
            length += 1
            code = (code << 8) | (self.prefix & 0xFF)
        return code.to_bytes(length=length, byteorder="little")


class OperandEncoding(Enum):
    ADD = "add",  # po + r r/m
    RM = "rm",  # po r/m, reg
    MR = "mr",  # po reg, r/m
    MI = "mi",  # po r/m, imm


class OperandType(Enum):
    # register
    R8 = "r8",
    R16 = "r16",
    R32 = "r32",

    # memory
    M8 = "m8",
    M16 = "m16",
    M32 = "m32",

    # immediate
    I8 = "i8",
    I16 = "i16",
    I32 = "i32",


# represents one encoding of an instruction
class InstructionEncoding:
    def __init__(
        self,
        mnemonic: str,
        opcode: Opcode,
        operand_encoding: OperandEncoding,
        operands: list[OperandType],
    ):
        self.mnemonic: Final = mnemonic
        self.opcode: Final = opcode
        self.operand_encoding: Final = operand_encoding
        self.operands: Final = operands


class Register:
    def __init__(self, reg: int, r8: str, r16: str, r32: str, sreg: str):
        self.reg: Final = reg & 0x7  # 3 bits
        self.r8: Final = r8
        self.r16: Final = r16
        self.r32: Final = r32
        self.sreg: Final = sreg


class Operand:
    def __init__(self, reg: Register, type: OperandType):
        self.reg: Final = reg
        self.type: Final = type


class Instruction:
    def __init__(self, encoding: InstructionEncoding, operands: list[Operand]):
        self.encoding: Final = encoding
        self.operands: Final = operands
