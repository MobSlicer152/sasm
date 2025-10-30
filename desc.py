# this file handles loading x86.json

import json

from encoder import Opcode, InstructionEncoding, OperandType, OperandEncoding, Register, RegisterType

class Desc:
    def __init__(self, path: str):
        desc = None
        with open(path, "r") as f:
            desc = json.load(f)

        self.registers: dict[str, Register] = {}
        for mnem, info in desc["registers"].items():
            self.registers[mnem] = Register(mnem, RegisterType(info["type"]), int(info["reg"]))

        self.instructions: dict[str, InstructionEncoding] = {}
        for instr in desc["instructions"]:
            mnem = instr["mnemonic"]
            operand_types = []
            for operand in instr["operands"]:
                types = []
                for type in operand:
                    types.append(OperandType(type))
                operand_types.append(types)

            self.instructions[mnem] = InstructionEncoding(mnem, Opcode(int(instr["opcode"]["primary"], 16)), OperandEncoding(instr["operand_encoding"]), operand_types)

    def __repr__(self):
        return f"Desc {{ registers: {self.registers}, instructions: {self.instructions} }}"
