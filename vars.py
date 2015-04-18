memory_stack = [None for i in xrange(40)]

symbol = {
	'00': 'begin',
	'01': 'end',
	'02': 'mod',
	'03': 'add',
	'04': 'sub',
	'05': 'cmp',
	'06': 'label',
	'10': 'read',
	'11': 'pushi',
	'12': 'pushv',
	'13': 'pop',
	'14': 'jmp',
	'15': 'jl',
	'16': 'jg',
	'17': 'jeq',
	'18': 'disp'
}

symbol_reversed = dict (zip(symbol.values(),symbol.keys()))
