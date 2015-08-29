"""Lindenmayer. Creates fractals from L-Systems.

Usage:
  lindenmayer.py [--out=<filename>] [--format=(svg|png)] (koch|levic|dragon) <iterations>
  lindenmayer.py (-h | --help)
  lindenmayer.py --version

Options:
  --version            Show version.
  -h --help            Show this screen.
  --out=<filename>     Specify output file name without ending [default: fractal]
  --format=<name>      Specify output format [default: svg]
  <iterations>         Number of iterations of the L-System. WARNING: Start low!
"""

from collections import namedtuple
from math import sin, cos, radians

from docopt import docopt
import cairosvg
import svgwrite

# A command is a named tuple whose first entry is 'name'
# followed by arbitrary payload
class Command(object):

	DrawForward = namedtuple('DrawForward', 'name')
	Turn = namedtuple('Turn', 'name deg')

	DRAW_FORWARD = 'drawForward'
	TURN = 'turn'

	@staticmethod
	def draw_forward():
		return Command.DrawForward(Command.DRAW_FORWARD,)

	@staticmethod
	def turn(deg):
		return Command.Turn(Command.TURN, deg)

class LSystem(object):
	
	def __init__(self, variables, constants, start, rules, commands):
		self.variables = variables
		self.constants = constants
		self.start = start
		self.rules = rules
		self.commands = commands

	def _generate(self, n):
		s = self.start
		for _ in range(n):
			tmp = ""
			for c in s:
				tmp += self.rules.get(c, c)
			s = tmp
		return s

	def _getCommands(self, s):
		return [self.commands[c] for c in s if c in self.commands]

	def _draw(self, n, stepsize):
		s = self._generate(n)
		commands = self._getCommands(s)

		x = y = rot = 0
		points = [(0,0)]
		
		for command in commands:
			if command.name == Command.DRAW_FORWARD:
				x += cos(rot) * stepsize
				y += sin(rot) * stepsize
				points.append((x,y))
			elif command.name == Command.TURN:
				rot += radians(command.deg)

		(xmin, ymin) = map(min, zip(*points))
		(xmax, ymax) = map(max, zip(*points))

		dwg = svgwrite.Drawing()
		curve = dwg.polyline(points=points, stroke='black', fill='none', stroke_width=1)
		dwg.add(curve)
		dwg.viewbox(xmin, ymin, xmax-xmin, ymax-ymin)
		return dwg

	def saveSvg(self, n, filename, stepsize=10):
		dwg = self._draw(n, stepsize)
		dwg.saveas(filename)

	def savePng(self, n, filename, stepsize=10):
		dwg = self._draw(n, stepsize)
		with open(filename, 'wb') as f:
			cairosvg.svg2png(bytestring=dwg.tostring(),write_to=f)

def koch_curve():
	variables = ['F']
	constants = ['+', '-']
	start = 'F'
	rules = {
		'F' : 'F+F-F-F+F'
	}

	commands = {
		'F' : Command.draw_forward(),
		'+' : Command.turn( 90),
		'-' : Command.turn(-90)
	}

	return LSystem(variables, constants, start, rules, commands)	

def dragon_curve():
	variables = ['X', 'Y']
	constants = ['F', '+', '-']
	start = 'FX'
	rules = {
		'X' : 'X+YF+',
		'Y' : '-FX-Y'
	}

	commands = {
		'F' : Command.draw_forward(),
		'+' : Command.turn( 90),
		'-' : Command.turn(-90)
	}

	return LSystem(variables, constants, start, rules, commands)	

def levi_c_curve():
	variables = ['F']
	constants = ['+', '-']
	start = 'F'
	rules = {
		'F' : '+F--F+'
	}

	commands = {
		'F' : Command.draw_forward(),
		'+' : Command.turn( 45),
		'-' : Command.turn(-45)
	}

	return LSystem(variables, constants, start, rules, commands)


if __name__ == '__main__':
	arguments = docopt(__doc__, version='Lindenmayer 0.1')
	print(arguments)

	fmt = arguments['--format']
	filename = arguments['--out']
	iterations = int(arguments['<iterations>'])

	outputpath = filename + '.' + fmt

	if arguments['koch']:
		system = koch_curve()
	elif arguments['levic']:
		system = levi_c_curve()
	elif arguments['dragon']:
		system = dragon_curve()

	if fmt == 'svg':
		system.saveSvg(iterations, outputpath, stepsize=10)
	elif fmt == 'png':
		system.savePng(iterations, outputpath, stepsize=10)

