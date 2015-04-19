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
		for i in xrange(30,39):
			if not vars.memory_stack[i] or vars.memory_stack[i] == variable:
				vars.memory_stack[i] = variable
				return i

		return False

	def write_mla_to_file(self, mla):
		with open('input.mla', 'w+') as output_file:
			for line in mla:
				output_file.write(line+'\n')

	def execute(self, mla_code, parent=None):
		memory_stack = [None for i in xrange(40)]
		stack_register = []

		for i in range(0, len(mla_code)):
			memory_stack[i] = mla_code[i]

		i = 0
		while i < 30:
			if not memory_stack[i]:
				break

			instruction = memory_stack[i][0:2]
			param = int(memory_stack[i][2:4])

			print instruction, param
			if vars.symbol[instruction] == "read":
				# val = input("Input a value for N: ")
				parent.getinput.emit()
				val = queue.get()
				memory_stack[param] = val
			elif vars.symbol[instruction] == "mod":
				if len(stack_register) < 2:
					print "Null Operand Error."
					return

				a = stack_register.pop()
				b = stack_register.pop()

				stack_register.append(b % a)
			elif vars.symbol[instruction] == "add":
				if len(stack_register) < 2:
					print "Null Operand Error."
					return

				a = stack_register.pop()
				b = stack_register.pop()

				if (a+b) > 99:
					print "Overflow Error."
					return

				stack_register.append(b + a)
			elif vars.symbol[instruction] == "sub":
				if len(stack_register) < 2:
					print "Null Operand Error."
					return

				a = stack_register.pop()
				b = stack_register.pop()

				if (b - a) < 0:
					print "Overflow Error."
					return

				stack_register.append(b - a)
			elif vars.symbol[instruction] == "cmp":
				if len(stack_register) < 2:
					print "Null Operand Error."
					return

				a = stack_register.pop()
				b = stack_register.pop()

				stack_register.append(a == b)
			elif vars.symbol[instruction] == "pushi":
				if len(stack_register) == 5:
					print "Stack Overflow Error."
					return

				stack_register.append(param)
			elif vars.symbol[instruction] == "pushv":
				if len(stack_register) == 5:
					print "Stack Overflow Error."
					return

				stack_register.append(memory_stack[param])
			elif vars.symbol[instruction] == "pop":
				if not stack_register:
					print "Empty Stack Error."
					return

				memory_stack[param] = stack_register.pop()
			elif vars.symbol[instruction] == "jmp":
				i = param - 2
			elif vars.symbol[instruction] == "jl":
				if len(stack_register) < 2:
					print "Null Compare Error."
					return
				elif stack_register[-1] < stack_register[-2]:
					i = param - 2
			elif vars.symbol[instruction] == "jg":
				if len(stack_register) < 2:
					print "Null Compare Error."
					return
				elif stack_register[-1] > stack_register[-2]:
					i = param - 2
			elif vars.symbol[instruction] == "jeq":
				if len(stack_register) < 2:
					print "Null Compare Error."
					return
				elif stack_register[-1] == stack_register[-2]:
					i = param - 2
			elif vars.symbol[instruction] == "disp":
				print memory_stack[param]
			elif vars.symbol[instruction] == "end":
				break
			
			i += 1

			print stack_register


		print memory_stack
		print stack_register

		

# assembler = AssemBER.Instance()
# mla_code = AssemBER.Instance().convert(codes)
# assembler.write_mla_to_file(mla_code)
# assembler.execute(mla_code)