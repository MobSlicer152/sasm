# this file handles encoding instructions

from enum import StrEnum
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

    def __repr__(self):
        secondary = None if self.secondary is None else f"0x{self.secondary:02X}"
        prefix = None if self.prefix is None else f"0x{self.prefix:02X}"
        return f"Opcode {{ primary: 0x{self.primary:02X}, secondary: {secondary}, prefix: {prefix}, has_0f: {self.has_0f}, encoded: {self.encode()} }}"


class OperandEncoding(StrEnum):
    ADD = "add",  # po + r r/m
    RM = "rm",  # po r/m, reg
    MR = "mr",  # po reg, r/m
    MI = "mi",  # po r/m, imm


class RegisterType(StrEnum):
    R8 = "r8",
    R16 = "r16",
    R32 = "r32",
    SREG = "sreg",
    EEE = "eee"


class OperandType(StrEnum):
    # register
    R8 = RegisterType.R8,
    R16 = RegisterType.R16,
    R32 = RegisterType.R32,
    SREG = RegisterType.SREG,
    EEE = RegisterType.EEE,

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
        operands: list[list[OperandType]],
    ):
        self.mnemonic: Final = mnemonic
        self.opcode: Final = opcode
        self.operand_encoding: Final = operand_encoding
        self.operands: Final = operands

    def __repr__(self):
        return f"InstructionEncoding {{ mnemonic: {self.mnemonic}, opcode: {self.opcode}, operand_encoding: {self.operand_encoding}, operands: {self.operands} }}"


# represents one register. different sizes of the same register are considered distinct for simplicity.
class Register:
    def __init__(self, name: str, type: RegisterType, reg: int):
        self.name: Final = name
        self.type: Final = type
        self.reg: Final = reg & 0x7  # 3 bits

    def __repr__(self):
        return f"Register {{ name: {self.name}, type: {self.type}, reg: {self.reg} }}"


# represents an operand.
class Operand:
    def __init__(self, reg: Register, type: OperandType, disp: int | None = None):
        self.reg: Final = reg
        self.type: Final = type
        self.disp: Final = disp
        if self.disp is not None:
            self.addr: Final = True

    # TODO: scaled index support?


class Instruction:
    def __init__(self, encoding: InstructionEncoding, operands: list[Operand]):
        self.encoding: Final = encoding
        self.operands: Final = operands
