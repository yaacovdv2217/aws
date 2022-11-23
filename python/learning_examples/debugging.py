# debugging trick:
def add(first, last):
	return first + last


add(1, 2)
import pdb
pdb.set_trace()
add(1, 'two')
