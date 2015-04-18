import vars
import sys

print vars.memory_stack
asmfile = 'input.asm'

with open(asmfile, 'r') as input_file:
	codes = [i.strip() for i in input_file.readlines()]

class AssemBER(object):
	def convert(self, codes):
		mla = []

		for code in codes:
			arr = code.split(' ')
			instruction = arr[0]

			if instruction in vars.symbol_reversed:
				mc = vars.symbol_reversed[instruction]
				if mc[0] == '0':
					mc += '00'
					mla.append(mc)
				else:
					address = self.append_to_stack(arr[1])
					if not address:
						print "ERROR BAYET MAYGAD"
					else:
						mc += str(address)
						mla.append(mc)

					print address

	def append_to_stack(self, variable):
		print variable
		for i in xrange(30,39):
			if not vars.memory_stack[i] or vars.memory_stack[i] == variable:
				vars.memory_stack[i] = variable
				return i

		return False




test = Bersembler().convert(codes)
