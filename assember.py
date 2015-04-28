import sys
import vars
from Singleton import Singleton
from AppQueue import queue

# asmfile = 'input.asm'

# with open(asmfile, 'r') as input_file:
# 	codes = [i.strip() for i in input_file.readlines()]


@Singleton
class AssemBER(object):
    def convert(self, codes):
        self.clear_vars_mem_stack()
        mla = []
        labels = {}

        if codes[0] != 'begin':
            print "Error. Program should start with a 'begin' instruction"
            return 0, True

        for i in xrange(0, len(codes)):
            instruction = codes[i]

            if instruction.endswith(':'):
                labels[instruction] = str(i + 1)

        for x, code in enumerate(codes):
            arr = code.split(' ')
            instruction = arr[0]

            if instruction == 'begin' and x != 0:
                print "Misplaced 'begin' instruction"
                return x, True

            if instruction in vars.symbol_reversed:
                mc = vars.symbol_reversed[instruction]
                if mc[0] == '0':
                    if len(arr) == 2 and not arr[1] == "":
                        print instruction, "does not take any parameters"
                        return x, True
                    else:
                        mc += '00'
                        mla.append(mc)
                        if mc == '0100':
                            break
                else:
                    if not len(arr) == 2 or arr[1] == "":
                        print instruction, "expects parameters, none given"
                        return x, True
                    else:
                        if mc == '11':
                            if int(arr[1]) < 10:
                                mc += '0' + arr[1]
                            else:
                                mc += arr[1]
                            mla.append(mc)
                        elif mc in ['14', '15', '16', '17']:
                            arr[1] += ":"
                            if arr[1] in labels:
                                mla.append(mc + str(labels[arr[1]]))
                            else:
                                print "Label not found"
                                return x, True
                        else:
                            address = self.append_variable_to_stack(arr[1])
                            if not address:
                                print "Memory full."
                            else:
                                mc += str(address)
                                mla.append(mc)

            elif instruction.endswith(':'):
                if int(labels[instruction]) < 10:
                    labels[instruction] = '0' + labels[instruction]

                mla.append('06' + labels[instruction])
            else:
                print instruction + " is not supported."
                return x, True

        return mla, False

    def clear_vars_mem_stack(self):
        vars.memory_stack = [None for i in xrange(40)]

    def append_variable_to_stack(self, variable):
        for i in xrange(30, 39):
            if not vars.memory_stack[i] or vars.memory_stack[i] == variable:
                vars.memory_stack[i] = variable
                return i

        return False

    def write_mla_to_file(self, mla):
        with open('input.mla', 'w+') as output_file:
            for line in mla:
                output_file.write(line+'\n')

    def execute_line(self, linenum, parent=None):
        mla_line = self.memory_stack[linenum]
        instruction = mla_line[0:2]
        param = int(mla_line[2:4])

        if instruction in vars.symbol:
            if vars.symbol[instruction] == "read":
                # val = input("Input a value for N: ")
                # self.memory_stack[param] = val
                return self.read(param, parent)
            elif vars.symbol[instruction] == "mod":
                return self.arith_op('mod')
            elif vars.symbol[instruction] == "add":
                return self.arith_op('add')
            elif vars.symbol[instruction] == "sub":
                return self.arith_op('sub')
            elif vars.symbol[instruction] == "cmp":
                return self.arith_op('cmp')
            elif vars.symbol[instruction] == "pushi":
                return self.push('i', param)
            elif vars.symbol[instruction] == "pushv":
                return self.push('v', param)
            elif vars.symbol[instruction] == "pop":
                return self.pop(param)
            elif vars.symbol[instruction] == "jmp":
                return self.jmp('jmp', param)
            elif vars.symbol[instruction] == "jl":
                return self.jmp('jl', param)
            elif vars.symbol[instruction] == "jg":
                return self.jmp('jg', param)
            elif vars.symbol[instruction] == "jeq":
                return self.jmp('jeq', param)
            elif vars.symbol[instruction] == "disp":
                self.disp(param)
            elif vars.symbol[instruction] == "end":
                return None

            return True
        else:
            print "Instruction not supported",
            return False

    def execute(self, mla_code, parent=None):
        self.clear()
        self.loadcodetomem(mla_code)

        i = 0
        while i < 30:
            if not self.memory_stack[i]:
                break
            else:
                temp = self.execute_line(i, parent)
                if temp:
                    if type(temp) is int:
                        i = temp
                else:
                    if i < len(mla_code) - 1:
                        print "at line", i + 1
                        return True, i
                i += 1
        return False, None

    def loadcodetomem(self, mla_code):
        for i in range(0, len(mla_code)):
            self.memory_stack[i] = mla_code[i]

    def clear(self):
        self.memory_stack = [None for i in xrange(40)]
        self.stack_register = []

    def read(self, param, parent=None):
        if type(parent).__name__ is "ExecuteThread":
            parent.getinput.emit()
        else:
            parent.getinput()
        val = queue.get()
        if val is False:
            print "Execution terminated",
            return False
        else:
            self.memory_stack[param] = val
            return True

    def arith_op(self, op):
        if len(self.stack_register) < 2:
            print "Null Operand Error",
            return False

        if not self.stack_register[-1] or not self.stack_register[-2]:
            print "Unsupported operand type: 'NoneType'"
            return False

        a = self.stack_register.pop()
        b = self.stack_register.pop()

        if op == 'mod':
            self.stack_register.append(b % a)
        elif op == 'add':
            if (a+b) > 99:
                print "Overflow Error",
                return False

            self.stack_register.append(b + a)
        elif op == 'sub':
            if (b - a) < 0:
                print "Overflow Error",
                return False

            self.stack_register.append(b - a)
        else:
            self.stack_register.append(a == b)
        return True

    def push(self, push_type, param):
        if len(self.stack_register) == 5:
            print "Stack Overflow Error",
            return False

        if push_type == 'i':
            self.stack_register.append(param)
        else:
            self.stack_register.append(self.memory_stack[param])
        return True

    def pop(self, param):
        if not self.stack_register:
            print "Empty Stack Error",
            return False

        self.memory_stack[param] = self.stack_register.pop()
        return True

    def jmp(self, jmp_type, param):
        result = True
        if jmp_type in ['jl', 'jg', 'jeq']:
            if len(self.stack_register) < 2:
                print "Null Compare Error.",
                return False

            if jmp_type == 'jl' and not self.stack_register[-1] < self.stack_register[-2] or \
               jmp_type == 'jg' and not self.stack_register[-1] > self.stack_register[-2] or \
               jmp_type == 'jeq' and not self.stack_register[-1] == self.stack_register[-2]:
                result = False

        if result:
            return param - 2
        return True

    def disp(self, param):
        print self.memory_stack[param]

# assembler = AssemBER.Instance()
# mla_code = AssemBER.Instance().convert(codes)
# assembler.write_mla_to_file(mla_code)
# assembler.execute(mla_code)
