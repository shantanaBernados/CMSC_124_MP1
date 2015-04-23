import sys
import vars
from Singleton import Singleton
from AppQueue import queue


asmfile = 'input.asm'

with open(asmfile, 'r') as input_file:
	codes = [i.strip() for i in input_file.readlines()]

@Singleton
class AssemBER(object):
    def convert(self, codes):
        mla = []
        labels = {}

        for i in xrange(0, len(codes)):
            instruction = codes[i]

            if instruction.endswith(':'):
                labels[instruction] = str(i + 1)

        for code in codes:
            arr = code.split(' ')
            instruction = arr[0]

            if instruction in vars.symbol_reversed:
                mc = vars.symbol_reversed[instruction]
                if mc[0] == '0':
                    mc += '00'
                    mla.append(mc)
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
                            if int(labels[arr[1]]) < 10:
                                labels[arr[1]] = '0' + labels[arr[1]]

                            mla.append(mc + str(labels[arr[1]]))
                        else:
                            print "Label not found"
                            return
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
                return

        return mla

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

    def execute_line(self, mla_line, parent):
        print mla_line
        
        instruction = mla_line[0:2]
        param = int(mla_line[2:4])

        if vars.symbol[instruction] == "read":
            val = input("Input a value for N: ")
            self.memory_stack[param] = val
            # self.read(parent)
        elif vars.symbol[instruction] == "mod":
           self.arith_op('mod')
        elif vars.symbol[instruction] == "add":
           self.arith_op('add')
        elif vars.symbol[instruction] == "sub":
            self.arith_op('sub')
        elif vars.symbol[instruction] == "cmp":
           self.arith_op('cmp')
        elif vars.symbol[instruction] == "pushi":
            self.push('i', param)
        elif vars.symbol[instruction] == "pushv":
            self.push('v', param)
        elif vars.symbol[instruction] == "pop":
            self.pop(param)
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
            return

        print self.stack_register
        return 0

    def execute(self, mla_code, parent=None):
        self.memory_stack = [None for i in xrange(40)]
        self.stack_register = []

        for i in range(0, len(mla_code)):
            self.memory_stack[i] = mla_code[i]

        i = 0
        while i < 30:
            if not self.memory_stack[i]:
                break
            else:
                temp = self.execute_line(self.memory_stack[i], parent)
                if temp:
                    i = temp
                i += 1
            
        print self.memory_stack
        print self.stack_register

    def read(self, parent=None):
        parent.getinput.emit()
        val = queue.get()
        self.memory_stack[param] = val

    def arith_op(self, op):
        if len(self.stack_register) < 2:
            print "Null Operand Error."
            return

        a = self.stack_register.pop()
        b = self.stack_register.pop()

        if op == 'mod':
            self.stack_register.append(b % a)
        elif op == 'add':
            if (a+b) > 99:
                print "Overflow Error."
                return

            self.stack_register.append(b + a)
        elif op == 'sub':
            if (b - a) < 0:
                print "Overflow Error."
                return

            self.stack_register.append(b - a)
        else:
            self.stack_register.append(a == b)

    def push(self, push_type, param):
        if len(self.stack_register) == 5:
            print "Stack Overflow Error."
            return

        if push_type == 'i':
            self.stack_register.append(param)
        else:
            self.stack_register.append(self.memory_stack[param])

    def pop(self, param):
        if not self.stack_register:
            print "Empty Stack Error."
            return

        self.memory_stack[param] = self.stack_register.pop()

    def jmp(self, jmp_type, param):
        result = True
        if jmp_type in ['jl', 'jg', 'jeq']:
            if len(self.stack_register) < 2:
                print "Null Compare Error."
                return

            if jmp_type == 'jl' and not self.stack_register[-1] < self.stack_register[-2] or \
                jmp_type == 'jg' and not self.stack_register[-1] > self.stack_register[-2] or \
                jmp_type == 'jeq' and not self.stack_register[-1] == self.stack_register[-2]:
                result = False

        if result:
            return param - 2

    def disp(self, param):
        print self.memory_stack[param]



assembler = AssemBER.Instance()
mla_code = AssemBER.Instance().convert(codes)
assembler.write_mla_to_file(mla_code)
assembler.execute(mla_code)
