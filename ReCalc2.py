# -*- coding: utf-8 -*-

'''
Author: Max Friedman
License: GPLv3
Title: ReCalc

This is a graphing calculator written in python 3.6.

It has a GUI made with tkinter that it will default to using if tkinter
is installed. It defines graphing and polar graphing classes. It
remembers every input it is given.

Usage:
	ReCalc [-vcV] [EXPRESSION ...]
	ReCalc [EXPRESSION ...]
	ReCalc [-vcV]
	ReCalc [--verbose --commandline --version]

Arguments:
	EXPRESSION    optional expression to start with

Options:
	-v, --verbose      verbose logging
	-c, --commandline  use the command line interface
	-V  --version      give the version of ReCalc

It can do:

Addition:
>>> simplify("4 + 9")
'13'

Subtraction:
>>> simplify("8-11")
'-3'

Multiplication:
>>> simplify("9*.5")
'4.5'

Division:
>>> simplify("9/3")
'3'

Exponents:
>>> simplify("4^2.5")
'32'

Logarithms:
>>> simplify("log(16, 2)")
'4'

Trig Functions:
>>> simplify("sin(pi/2)")
'1'

Inverse Trig Functions:
>>> simplify("arcsin(0)")
'0'

Hyperbolic Functions:
>>> simplify("cosh(0)")
'1'

Inverse Hyperbolic Functions:
>>> simplify("arccosh(1)")
'0'

Ceiling Function:
>>> simplify("ceil(5.3)")
'6'

Floor Function:
>>> simplify("floor(11.9)")
'11'

Gauss Error Function:
>>> simplify("erf(0)")
'0'

Modulus:
>>> simplify("13 % 5")
'3'

Absolute Value:
>>> simplify("|8-10|")
'2'

Factorials:
>>> simplify("5!")
'120'

Gamma Function:
>>> simplify("gamma(5)")
'24'

Combinations:
>>> simplify("5C3")
'10'

Permutations:
>>> simplify("5P2")
'20'

Max:
>>> simplify("max(3, 4, 5, 2, -4)")
'5'

Min:
>>> simplify("min(4, 5, 12, -3, 4.5)")
'-3'

Mean:
>>> simplify("mean(5, 6, 12, 7)")
'7.5'

Median:
>>> simplify("median(3, 4, 3, 9, 7)")
'4'

Mode:
>>> simplify("mode(4, 3, 3 ,4 ,5, 5, 6, 4)")
'4'

Sample Standard Deviation:
>>> simplify("stdev(3, 4, 4, 6, 8)")
'2'

Definite Integrals:
>>> simplify("integral x*2 dx from 0 to 4")
'16'

Derivatives at a point:



Evaluating a Function at a Point:


Solving Equations:



and graphing functions in Cartesian and polar.
'''


'''  Completed
2) Make average functions deal with non-number arguments
3) Stdev
4) deal with commas
5) tkinter interface
8) min max functions
9) make tkinter windows close
12) two graphs at once
14) eval non-number arguments
15) multi argument functions cant have commas in the second argument
16) absolute value with pipes
17) use division sign
18) set y bounds on graphs
19) pickle degree mode
20) graph closes only when user dictates
22) unit conversions
28) improve tkinter interface
29) cut off trailing zeros
30) two expressions adjacent means multiplication
31) polar graphs
33) show request
37) other weird trig functions
40) doc strings for all of the tests that need them
43) save graphs
44) on fedora only one enter key is bound in the GUI
45) parametric functions
46) log errors
47) don't stop the program when there is an error
48) fix error when you close a polar graphing window early
50) move gamma into one_arg_funcs
51) make the delete button delete all of multi-letter fuctions other
buttons put there
52) allow 'y =' in graphs
53) put cursor in entry box on startup
55) don't move cursor to end of line when backspace is hit
57) unit detection will only use first part is the first part is another
unit
'''

'''  To Do
1) Deal with floating point errors
6) complex numbers
7) higher order derivatives
10) graph non-functions
11) improper integrals
13) integrals can have non-number bounds
14) derivatives non-number arguments
21) matrices
23) indefinite integrals
24) derivatives of functions
25) summation notation
26) big pi notation
27) series
32) 3d graphs
34) make icon of tkinter window when run on Fedora
35) make compatible with other operating systems
36) fix subtraction problem
38) setup and wheel files
39) make tests for all parts of the program
41) user defined functions
42) user defined variables
49) don't let the user pass ln(x) multiple arguments
54) error handling for passing graph functions incorrectly
56) manipulate units
58)
'''


#  Windows:
#  C:\Users\Max\Documents\Python\ReCalc\ReCalc.py
#  Bash:
#  C:/Users/Max/Documents/Python/ReCalc/ReCalc.py

import math
import statistics as stats
import sys
import os
import logging

from atexit import register
from warnings import warn, simplefilter
from pickle import load, dump
from itertools import chain

version = "0.1.12"

logger = logging.getLogger("ReCalc_logger")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("log_file.log", encoding = "UTF-8")
if "-v" in sys.argv:
	fh.setLevel(logging.DEBUG)
else:
	fh.setLevel(logging.INFO)

formatter = logging.Formatter(
	"{levelname:<8s}: {message:s}",
	style = "{")
fh.setFormatter(formatter)

logger.addHandler(fh)

logger.info("Program is starting.")

# import sympy if installed
try:
	from sympy import symbols, integrate, sympify
	from sympy.solvers import solve
except ModuleNotFoundError:
	logger.warning("Sympy could not be imported.")
	simplefilter("default", ImportWarning)
	warn(
		("Sympy can not be imported. Solving equations and definite "
			"integrals will not be available."),
		category = ImportWarning)

# import tkinter if installed
try:
	import tkinter as tk
	from tkinter import filedialog
	from _tkinter import TclError
	from PIL import ImageTk
except ModuleNotFoundError:
	logger.warning("Tkinter could not be imported.")
	simplefilter("default", ImportWarning)
	warn(
		"Tkinter can not be imported. Using command line interface",
		category = ImportWarning)

# import numpy if installed
try:
	import numpy as np
except ModuleNotFoundError:
	logger.warning("Numpy could not be imported.")
	simplefilter("default", ImportWarning)
	warn(
		"Numpy can not be imported. Can not graph",
		category = ImportWarning)

# import Pillow if installed
try:
	from PIL import Image
except ModuleNotFoundError:
	logger.warning("Pillow could not be imported.")
	simplefilter("default", ImportWarning)
	warn(
		"Pillow can not be imported. Can not graph",
		category = ImportWarning)

# import docopt if installed
try:
	from docopt import docopt
except ModuleNotFoundError:
	logger.warning("Docopt could not be imported.")
	simplefilter("default", ImportWarning)
	warn(
		"Docopt could not be imported command line arguments may not "
		"work.",
		category = ImportWarning)

# import regex if installed
try:
	import regex as re
except ModuleNotFoundError:
	logger.warning("Regex could not be imported.")
	simplefilter("default", ImportWarning)
	warn("Regex could not be imported and somethings may be case sensative "
		"when they should not be.",
		category = ImportWarning)
	import re

from ReCalc_objects import *

def compile_ignore_case(regex):
	return re.compile("(?i:" + regex + ")")


logger.info("operating system: %s", os.name)

up_hist = 0

# changeable variables
use_gui = True
graph_w = 400
graph_h = 400
graph_colors = ("black", "red", "blue", "green", "orange", "purple")



key_binds = {
	"nt": {13: "enter", 38: "up", 40: "down", 8: "backspace"},
	"posix": {104: "enter", 36: "enter", 111: "up", 116: "down"},
}

g_bound_names = (
	"x min", "x max",
	"y min", "y max",
	"theta min", "theta max",
)

one_arg_funcs = {

	# the order of which functions come first matters because if trig
	# functions come before hyperbolic functions the "h" is
	# interpreted as part of the argument for the function.

	#   name                 function                angles
	"hacovercosin": (lambda x: .5 + math.sin(x) / 2, "in"),
	"hacoversin": (lambda x: .5 - math.sin(x) / 2, "in"),
	"havercosin": (lambda x: .5 + math.cos(x) / 2, "in"),
	"haversin": (lambda x: .5 - math.cos(x) / 2, "in"),
	"covercosin": (lambda x: 1 + math.sin(x), "in"),
	"coversin": (lambda x: 1 - math.sin(x), "in"),
	"vercosin": (lambda x: 1 + math.cos(x), "in"),
	"versin": (lambda x: 1 - math.cos(x), "in"),
	"exsec": (lambda x: 1 / math.cos(x) - 1, "in"),
	"excsc": (lambda x: 1 / math.sin(x) - 1, "in"),

	"asinh": (math.asinh, "out"),
	"acosh": (math.acosh, "out"),
	"atanh": (math.atanh, "out"),
	"asech": (lambda x: math.acosh(1 / x), "out"),
	"acsch": (lambda x: math.asinh(1 / x), "out"),
	"acoth": (lambda x: math.atanh(1 / x), "out"),

	"arcsinh": (math.asinh, "out"),
	"arccosh": (math.acosh, "out"),
	"arctanh": (math.atanh, "out"),
	"arcsech": (lambda x: math.acosh(1 / x), "out"),
	"arccsch": (lambda x: math.asinh(1 / x), "out"),
	"arccoth": (lambda x: math.atanh(1 / x), "out"),

	"sinh": (math.sinh, "in"),
	"cosh": (math.cosh, "in"),
	"tanh": (math.tanh, "in"),
	"sech": (lambda x: 1 / math.cosh(x), "in"),
	"csch": (lambda x: 1 / math.sinh(x), "in"),
	"coth": (lambda x: 1 / math.tanh(x), "in"),

	"asin": (math.asin, "out"),
	"acos": (math.acos, "out"),
	"atan": (math.atan, "out"),
	"asec": (lambda x: math.acos(1 / x), "out"),
	"acsc": (lambda x: math.asin(1 / x), "out"),
	"acot": (lambda x: math.atan(1 / x), "out"),

	"arcsin": (math.asin, "out"),
	"arccos": (math.acos, "out"),
	"arctan": (math.atan, "out"),
	"arcsec": (lambda x: math.acos(1 / x), "out"),
	"arccsc": (lambda x: math.asin(1 / x), "out"),
	"arccot": (lambda x: math.atan(1 / x), "out"),

	"sin": (math.sin, "in"),
	"cos": (math.cos, "in"),
	"tan": (math.tan, "in"),
	"sec": (lambda x: 1 / math.cos(x), "in"),
	"csc": (lambda x: 1 / math.sin(x), "in"),
	"cot": (lambda x: 1 / math.tan(x), "in"),

	"abs": (math.fabs, ""),
	"ceil": (math.ceil, ""),
	"floor": (math.floor, ""),
	"erf": (math.erf, ""),
	"erfc": (math.erfc, ""),
	"gamma": (math.gamma, ""),
	"Γ": (math.gamma, ""),
}

list_functions = (
	*one_arg_funcs.keys(), "mod", "log", "ln", "average",
	"ave", "mean", "median", "mode", "max", "min", "stdev",
)

keywords = list_functions + (
	"convert", "graph", "history", "quit", "exit", "degree", "mode", "radian", "solve",
	"eval", "evaluate", "for", "at", "integral", "integrate", "from", "to", "derivative",
	"of", "with", "respect", "c", "p", "∫",)

# regex for a number
reg_num = "(-?[0-9]+\.?[0-9]*|-?[0-9]*\.?[0-9]+)"


units = tuple(map(
	lambda x: x.replace("^", "\^"),
	sort_by_length(chain.from_iterable((
		Unit.base_units,
		*Unit.nonbase_units.values())))))

# regular expressions
regular_expr = dict(

	# regex for commands
	# ^$ is for an empty string
	command_comp = compile_ignore_case(
		"(history)|(quit|exit|^$)|"
		"(degree mode)|(radian mode)"),

	implicet_mult_pre_const_comp = compile_ignore_case(
		"([.0-9])(?=e|pi|π|tau|τ|phi|φ|"
		+ "|".join(list_functions) + ")"),

	# regex for constants
	const_comp = compile_ignore_case(
		"(pi|π|(?<![a-z0-9])e(?![a-z0-9])|"
		"ans(?:wer)?|tau|τ|phi|φ)"),

	implicet_mult_comp = compile_ignore_case(
		"([.0-9])(?=[(x])|(\)\()"),

	# regex for graphing
	graph_comp = compile_ignore_case("graph (.+)"),

	# regex for equation solving
	alg_comp = compile_ignore_case("solve(.+)"),

	# regex for evaluating functions
	eval_comp = compile_ignore_case(
		"eval(?:uate)? (.+) (?:for|at) (.+)"),

	# regex for derivatives (must be at a number)
	der_comp = compile_ignore_case(
		"derivative of (.+) at (.+?)"
		"( with respect to [a-z])?"),

	# regex for integrals (bounds must be numbers)
	int_comp = compile_ignore_case(
		"(?:integra(?:te ?|l ?)|∫)(.+) ?d([a-z])"
		" (?:from )?" + reg_num + " to " + reg_num),

	# regex for converting between units
	# intentianly not using compile_ignore_case so that you can
	# differentiate between capital and lowercase units
	conv_comp = re.compile(
		"[Cc][Oo][Nn][Vv][Ee][Rr][Tt] (.+?)(?="
		+ "|".join(units) + ")(" + "|".join(units) + ") ?[Tt][Oo] ("
		+ "|".join(units) + ")"),

	# regex for combinations and permutations
	# parentheses is to differentiate it from choose notation
	comb_comp = compile_ignore_case("(c|p)(\(.+)"),

	# regex for statistics functions
	ave_comp = compile_ignore_case(
		"(average|ave|mean|median|mode|"
		"max|min|stdev)(.+)"),

	# regex for one argument functions
	trig_comp = compile_ignore_case(
		"(" + "|".join(one_arg_funcs.keys()) + ")(.+)"),

	# regex for logarithms
	log_comp = compile_ignore_case("log(.+)|ln(.+)"),

	# regex for modulus
	mod2_comp = compile_ignore_case("mod(.+)"),

	# regex for detecting absolute value
	abs_comp = compile_ignore_case("(.*\|.*)"),

	# here is where the order of operations starts to matter
	# it goes: parentheses, choose notation(nCm), exponents, factorial,
	# modulus, multiplication, addition

	# regex for parentheses
	# [^()] makes it only find the inner most parentheses
	paren_comp = compile_ignore_case("\(([^()]+)\)"),

	# ignores commas in the middle of numbers
	# could be problematic if two floats ever
	# end up next to each other
	comma_comp = compile_ignore_case(reg_num + "," + reg_num),

	# regex for choose notation (not recursive)
	# in the form of "nCm" or "nPm"
	choose_comp = compile_ignore_case(reg_num + " ?(c|p) ?" + reg_num),

	# regex for exponents (not recursive)
	exp_comp = compile_ignore_case(
		reg_num + " ?(\*\*|\^) ?" + reg_num),

	# regex for factorials (not recursive)
	fact_comp = compile_ignore_case(reg_num + "\!"),

	# regex in the form x % y (not recursive)
	mod_comp = compile_ignore_case(reg_num + " ?% ?" + reg_num),

	# regex for percentages (should probably be done without regex)
	per_comp = compile_ignore_case("%"),

	# regex for multiplication (not recursive)
	mult_comp = compile_ignore_case(reg_num + " ?([*/÷]) ?" + reg_num),

	# regex for addition (not recursive)
	add_comp = compile_ignore_case(reg_num + " ?([+-]) ?" + reg_num),
	
	# regex for variable assignment
	assign_comp = re.compile("([^=]+) ?= ?([^=]+)"),
)


class NumpyGraph(Graph):
	'''
	Cartesian Graphing window class using numpy and PIL.
	'''

	def __init__(
		self,
		xmin = -5, xmax = 5, ymin = -5, ymax = 5,
		wide = 400, high = 400):
		'''
		Initialize the graphing window.
		'''

		super().__init__(
			xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax,
			wide = wide, high = high)

		self.data = np.zeros(
			(self.high, self.wide, 3),
			dtype = np.uint8)
		self.data.fill(255)

		# create the image
		self.pic = ImageTk.PhotoImage(
			Image.fromarray(self.data, "RGB"))
		self.screen.create_image(
			self.wide / 2, self.high / 2, image = self.pic)

		# draws the axes
		self.axes()

	# draw the axes
	def axes(self):
		'''
		Draw the axis.
		'''

		# adjusted y coordinate of x-axis
		b = self.high + (self.ymin * self.high / self.yrang)

		# adjusted x coordinate of y-axis
		a = -1 * self.xmin * self.wide / self.xrang

		try:
			self.data[int(round(b, 0)), :, :] = 0
		except IndexError:
			pass
		try:
			self.data[:, int(round(a, 0)), :] = 0
		except IndexError:
			pass

		self.pic = ImageTk.PhotoImage(Image.fromarray(self.data, "RGB"))
		self.screen.create_image(
			self.wide / 2, self.high / 2, image = self.pic)

		try:
			self.root.update()
		except TclError:
			pass

	def draw(self, func, color = "black"):
		'''
		Draw a Cartesian function.
		'''

		pixel_color = Graph.color_dict[color]

		for i in range(self.data.shape[1]):

			x = i * self.xrang / self.wide + self.xmin
			y = float(evaluate(func, str(x)))
			a = int(round((x - self.xmin) * self.wide / self.xrang, 0))
			b = int(round(
				self.high - (y - self.ymin) * self.high / self.yrang,
				0))

			if 0 < b and b < self.high:
				self.data[b, i] = pixel_color

			self.image = Image.fromarray(self.data, "RGB")
			self.pic = ImageTk.PhotoImage(self.image)
			self.screen.create_image(
				self.wide / 2, self.high / 2, image = self.pic)

			self.root.update()


class NumpyPolarGraph(NumpyGraph):
	'''
	A polar graph using PIL and Numpy.
	'''

	def __init__(
		self,
		xmin = -5, xmax = 5, ymin = -5, ymax = 5,
		theta_min = 0, theta_max = 10,
		wide = 400, high = 400):

		super().__init__(
			xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax,
			wide = wide, high = high)

		self.theta_min = theta_min
		self.theta_max = theta_max

		self.theta_rang = self.theta_max - self.theta_min

	def draw(self, func, color = "black"):
		'''
		Draw a polar function with numpy.
		'''

		density = 1000
		theta = self.theta_min

		pixel_color = Graph.color_dict[color]

		while theta < self.theta_max:

			# move theta a little
			theta += self.theta_rang / density
			try:
				# eval the function at theta and set that to r
				r = float(evaluate(func, str(theta)))

				# find the slope at the point using find_derivative
				slope = float(find_derivative(func, str(theta)))

				x = r * math.cos(theta)
				y = r * math.sin(theta)

				# calculate how dense the points need to be
				# this function is somewhat arbitrary
				density = int((400 * math.fabs(slope)) + 500)

				# check if the graph goes off the screen
				if y > self.ymax or y < self.ymin or \
					x > self.xmax or x < self.xmin and density > 2000:
					denstiy = 2000

				# adjust coordinate for the
				# screen (this is the hard part)
				a = int(round(
					(x - self.xmin) * self.wide / self.xrang,
					0))
				b = int(round(
						self.high - (
							(y - self.ymin) * self.high / self.yrang),
						0))

				# draw the point
				if 0 < b and b < self.high and 0 < a and a < self.wide:
					self.data[b, a] = pixel_color
				self.image = Image.fromarray(self.data, "RGB")
				self.pic = ImageTk.PhotoImage(self.image)
				self.screen.create_image(
					self.wide / 2, self.high / 2, image = self.pic)

			except (ValueError,) as e:
				pass

			# update the screen
			try:
				self.root.update()
			except TclError as e:
				theta = self.theta_max + 1


class NumpyParameticGraph(NumpyGraph):
	'''
	A Parametic graphing class.
	'''

	def __init__(
		self,
		xmin = -5, xmax = 5, ymin = -5, ymax = 5,
		tmin = 0, tmax = 10,
		wide = 400, high = 400):
		'''
		Initialize the graphing object.
		'''

		super().__init__(
			xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax,
			wide = wide, high = high)

		self.tmin = tmin
		self.tmax = tmax

		self.trang = self.tmax - self.tmin

	def draw(self, funcs, color = "black"):
		'''
		Draw a parametric function.
		'''

		density = 1000
		t = self.tmin

		
		xfunc = funcs["x"]
		yfunc = funcs["y"]
		

		pixel_color = Graph.color_dict[color]

		while t < self.tmax:

			# move theta a little
			t += self.trang / density
			try:
				x = float(evaluate(xfunc, str(t), var = "t"))
				y = float(evaluate(yfunc, str(t), var = "t"))

				# adjust coordinate for the
				# screen (this is the hard part)
				a = int(round(
					(x - self.xmin) * self.wide / self.xrang,
					0))
				b = int(round(
						self.high - (
							(y - self.ymin) * self.high / self.yrang),
						0))

				# draw the point
				if 0 < b and b < self.high and 0 < a and a < self.wide:
					self.data[b, a] = pixel_color
				self.image = Image.fromarray(self.data, "RGB")
				self.pic = ImageTk.PhotoImage(self.image)
				self.screen.create_image(
					self.wide / 2, self.high / 2, image = self.pic)

			except (ValueError, TclError) as e:
				pass

			# update the screen
			try:
				self.root.update()
			except TclError as e:
				theta = self.tmax + 1


# multi session variables
try:
	calc_path = os.path.abspath(os.path.dirname(__file__))
	with open(
		os.path.join(calc_path, "ReCalc_info.txt"),
		"rb") as file:
		calc_info = load(file)
	history = calc_info["history"]
	ans = calc_info["ans"]
	# in degree mode 0 = off 2 = on
	degree_mode = calc_info["degree_mode"]
	polar_mode = calc_info["polar_mode"]
	der_approx = calc_info["der_approx"]
	hist_len = calc_info["hist_len"]
	win_bound = calc_info["window_bounds"]
except Exception as e:
	logger.warning("Loading settings failed. %s", str(e))

	history = NonRepeatingList()
	ans = 0
	degree_mode = 0
	polar_mode = False
	der_approx = .0001
	hist_len = 100
	win_bound = {
		"x min": -5,
		"x max": 5,
		"y min": -5,
		"y max": 5,
		"theta min": 0,
		"theta max": 10,
	}


constant_dict = {
	"pi": math.pi, "π": math.pi, "e": math.e,
	"ans": ans, "answer": ans, "tau": math.tau, "τ": math.tau,
	"phi": (1 + 5 ** 0.5) / 2, "φ": (1 + 5 ** 0.5) / 2,
}

def log_end():
	'''
	Log that the program is ending right before it ends.
	'''

	logger.info("Program is ending.")

register(log_end)


def find_y(s):
	'''
	Find x or y
	'''

	if polar_mode in ("Cartesian", "polar"):
		graph_y_comp = re.compile("y ?= ?(.+)")
		return re.search(graph_y_comp, s).group(1)
	elif polar_mode == "parametric":
		graph_y_comp = re.compile(
			"y ?= ?(.+) x ?= ?(.+)|x ?= ?(.+) y ?= ?(.+)")

	funcs = re.search(graph_y_comp, s)
	if funcs.group(1):
		d = {"y": funcs.group(1), "x": funcs.group(2)}
	elif funcs.group(3):
		d = {"x": funcs.group(3), "y": funcs.group(4)}

	return d


def save_info(**kwargs):
	'''
	Save settings to a file.
	'''

	calc_info.update(kwargs)

	with open(os.path.join(
		calc_path,
		"ReCalc_info.txt"), "wb") as file:
		dump(calc_info, file)


def delete_history():
	'''
	Delete the list of previous inputs.
	'''

	global up_hist

	up_hist = 0
	history.clear()
	save_info(history = history)


def switch_degree_mode(mode):
	'''
	Switch between degree mode and radian mode.

	Accept 'degree', 'radian', 0, 2, True, or False.
	Otherwise raise CalculatorError.
	'''

	global degree_mode

	if mode == "degree":
		degree_mode = 2
	elif mode == "radian":
		degree_mode = 0
	elif mode in (0, 2):
		degree_mode = mode
	elif mode is True:
		degree_mode = 2
	elif mode is False:
		degree_mode = 0
	else:
		raise CalculatorError("Can not set degree_mode to '%s'" % mode)

	save_info(degree_mode = degree_mode)


def switch_polar_mode(mode):
	'''
	Switch between polar and Cartesian graphing.

	Only accept 'polar', 'Cartesian', 'parametric' as inputs.
	Otherwise raise CalculatorError.
	'''

	global polar_mode

	if mode == "polar":
		polar_mode = mode
	elif mode == "Cartesian":
		polar_mode = mode
	elif mode == "parametric":
		polar_mode = mode
	else:
		raise CalculatorError("Can not set polar_mode to '%s'" % mode)

	save_info(polar_mode = polar_mode)


def change_hist_len(entry_box, root):
	'''
	Change the length of the history print back.

	Only accept integers greater than zero as valid lengths.
	'''

	global hist_len

	# get user input
	input = entry_box.get()

	# if the input is a digit set that to be the
	# history print back length save and close the window
	if input.isdigit() and int(input) > 0:
		hist_len = int(input)
		save_info(hist_len = hist_len)

		root.destroy()
	else:
		pass


def change_hist_len_win():
	'''
	Create a popup to change the length of the
	history print back.
	'''

	root = tk.Toplevel()

	# create window text
	disp = tk.Message(
		root,
		text = "Current History print back length: " + str(hist_len))
	disp.grid(row = 0, column = 0)

	# create the input box
	entry_box = tk.Entry(root)
	entry_box.grid(row = 1, column = 0)

	# bind enter to setting the input to be the history length
	root.bind(
		"<Return>",
		lambda event: change_hist_len(entry_box, root))

	root.mainloop()


def change_der_approx(entry_box, root):
	'''
	Change the length of the history print back.
	'''

	global der_approx

	# get user input
	input = entry_box.get()

	# if the input is a positive float set that to be the
	# der_approx value save and close the window
	if check_if_float(input) and "-" not in input:
		der_approx = float(input)
		save_info(der_approx = der_approx)

		root.destroy()
	else:
		pass


def change_der_approx_win():
	'''
	Create a popup to change the length of the
	history print back.
	'''

	root = tk.Toplevel()

	# create window text
	disp = tk.Message(
		root,
		text = "Current der approx: " + str(der_approx))
	disp.grid(row = 0, column = 0)

	# create the input box
	entry_box = tk.Entry(root)
	entry_box.grid(row = 1, column = 0)

	# bind enter to setting the input to be the history length
	root.bind(
		"<Return>",
		lambda event: change_der_approx(entry_box, root))

	root.mainloop()


def change_graph_win_set():
	'''
	Change the graphing window bounds.
	'''

	global win_bound, g_bound_entry, g_bound_string

	g_bound_input = {}
	for i in g_bound_names:
		g_bound_input[i] = g_bound_entry[i].get()

	for i in g_bound_names:
		if check_if_float(g_bound_input[i]):
			win_bound[i] = float(g_bound_input[i])

	save_info(win_bound = win_bound)

	for i in g_bound_names:
		g_bound_string[i].set("%s = %s" % (i, win_bound[i]))


#####################
# List of Functions #
#####################

def constant(constant):
	'''
	Evaluate mathematical constants.

	>>> constant("pi")
	3.141592653589793

	>>> constant("phi")
	1.618033988749895
	'''

	global constant_dict
	
	constant_dict["ans"] = ans
	constant_dict["answer"] = ans

	logger.debug(
		"constant has recieved '{constant}'".format(
			constant = constant))

	if constant in constant_dict:
		return constant_dict[constant]
	elif constant.lower() in constant_dict:
		return constant_dict[constant.lower()]
	else:
		raise CalculatorError(
			"'%s' is not a recognized constant." % constant)


def graph_function(func_arg):
	'''
	Graph the given function or functions.

	Call NumpyGraph or NumpyPolarGraph to graph given functions.
	Split into multiple function based on the location of the word and
	graph each of them separately iterating over a list to determine
	the color the the function is. It will repeat if you try and graph
	more functions than there are colors. If the statement ends with
	'from [number1] to [number2]' it will show the graph with x min as
	number1 and x max as number2.
	'''

	# check for bounds on graph
	graph_rang_comp = compile_ignore_case(
		"(.+(?=from))(from " + reg_num + " to " + reg_num + ")")

	# looks for x bounds on the graph
	range_m = re.search(graph_rang_comp, func_arg)
	if range_m is not None:
		logger.debug(
			"graph_function has detected the range: '{bound}' in "
			"'{arg}'".format(bound = range_m.groups(), arg = func_arg))

		func_arg = range_m

	# checks to see if tkinter is installed to graph things at all
	if set(("tkinter", "numpy", "PIL")).issubset(sys.modules):

		# finds multiple functions to graph
		if range_m is None:
			funcs_to_graph = func_arg.split(" and ")
		else:
			funcs_to_graph = func_arg.group(1).split(" and ")

		# sets bounds to bounds given
		if range_m is None:
			temp_graph_xmin = win_bound["x min"]
			temp_graph_xmax = win_bound["x max"]
		else:
			temp_graph_xmin = float(func_arg.group(3))
			temp_graph_xmax = float(func_arg.group(4))

		logger.debug(
			"graphing: {funcs}, from: {min}, to: {max}".format(
				funcs = funcs_to_graph,
				min = temp_graph_xmin,
				max = temp_graph_xmax))

		if any(filter(lambda a: "=" in a, funcs_to_graph)):
			funcs_to_graph = list(map(find_y, funcs_to_graph))

		# creates graph object
		if polar_mode == "Cartesian":
			made_graph = NumpyGraph(
				xmin = temp_graph_xmin, xmax = temp_graph_xmax,
				ymin = win_bound["y min"], ymax = win_bound["y max"],
				wide = graph_w, high = graph_h)
		elif polar_mode == "polar":
			made_graph = NumpyPolarGraph(
				xmin = temp_graph_xmin, xmax = temp_graph_xmax,
				ymin = win_bound["y min"], ymax = win_bound["y max"],
				theta_min = win_bound["theta min"],
				theta_max = win_bound["theta max"],
				wide = graph_w, high = graph_h)
		elif polar_mode == "parametric":
			made_graph = NumpyParameticGraph(
				xmin = temp_graph_xmin, xmax = temp_graph_xmax,
				ymin = win_bound["y min"], ymax = win_bound["y max"],
				tmin = win_bound["theta min"],
				tmax = win_bound["theta max"],
				wide = graph_w, high = graph_h)

		# works out how many times it needs to
		# loop the colors its using
		color_loops = math.ceil(
			len(funcs_to_graph) / len(graph_colors))

		# passes functions to be graphed and the color to do so with
		for f, c in zip(funcs_to_graph, graph_colors * color_loops):
			try:
				made_graph.draw(f, color = c)
			except TclError:
				pass

		# necessary for some of the tests
		return made_graph

	# informs the user of reason for failure
	else:
		raise CalculatorError(
			"Could not graph. Tkinter, Numpy, or PIL is not installed")


def solve_equations(equation):
	'''
	Solve equations

	Solve equations using sympy. If there is no equals
	sign it is assumed the expression equals zero. If there is more
	than one answer it will return a list of the answers.

	>>> solve_equations("x^2 = 4")
	[-2, 2]

	>>> solve_equations("x-7 = 13")
	20
	'''

	if "sympy" in sys.modules:
		# check for equals sign when solving equations
		eq_sides_comp = re.compile("(.+)=(.+)|(.+)")

		# checks for specified variable when solving equations
		alg_var_comp = re.compile("(.+) for ([a-z])")

		# find if there is a specified variable
		varm = re.search(alg_var_comp, equation)

		# find the variable its solving for. defaults to "x"
		if varm is None:
			x = symbols("x")
			eq = equation
		else:
			# used to be symbols(varm.group(2)[-1]) don't know why
			# may have been important
			x = symbols(varm.group(2))
			eq = varm.group(1)

		# if there is an equals sign solve for zero and use sympy
		# to solve it
		em = re.search(eq_sides_comp, eq)
		if em.group(3) is None:
			try:
				sym_zero = sympify(
					em.group(1) + "-(" + em.group(2) + ")")
				temp_result = solve(sym_zero, x)
			except (NotImplementedError, TypeError) as e:
				raise CalculatorError(str(e))

			# if there is only one result make it the result
			# otherwise return the list
			if len(temp_result) == 1:
				return temp_result[0]
			else:
				return temp_result

		# if there isn't an equals sign use sympy to solve
		else:
			temp_result = solve(em.group(3), x)

			# if there is only one result make it the result
			# otherwise return the list
			if len(temp_result) == 1:
				return temp_result[0]
			else:
				return temp_result
	else:
		raise CalculatorError(
			"Could not solve. Sympy not installed.")


def evaluate(expression, point, var = "x"):
	'''
	Evaluate the function by substituting var for the number you
	want to evaluate at.

	>>> evaluate("r^2", 5, var = "r")
	'25'

	>>> evaluate("3*b", "2", "b")
	'6'
	'''

	# substituting the point for x in the function and evaluating
	# that recursively
	return simplify(re.sub(
		"(?<![a-z])" + var + "(?![a-z])",
		str(point), expression, flags = re.I))


def find_derivative(expression, point, var = "x"):
	'''
	Calculate the derivate of the function at the given point

	Calculate the derivative by evaluating the slope
	between two points on either side of the point you are
	finding the derivative of with respect to var.
	'''

	# find the point on either side of the desired point
	p = float(simplify(point))
	x_one = p + der_approx
	x_two = p - der_approx

	# find the change in y value between the two points
	delta_y = (float(evaluate(
		expression, str(x_one), var = var))
		- float(evaluate(expression, str(x_two), var = var)))

	# divide by the length of the interval to find the slope
	return delta_y / (2 * der_approx)


def integrate_function(expression, var, a, b):
	'''
	Integrate with sympy.

	Integrals must be in a form that sympy can integrate.
	The bounds must be numbers not expressions.
	The integral must have a differential at the end of the function
	but before the bounds.
	'''

	if "sympy" in sys.modules:
		return float_to_str(integrate(expression, (var, a, b)))
	raise CalculatorError(
		"Could not integrate sympy is not installed.")


def convert(amount, start, end_units):
	'''
	Convert between different units.
	'''

	q = Unit(float(simplify(amount)), start)
	q.convert_inplace(end_units)
	return str(q)


def combinations_and_permutations(form, letter, n, m = None):
	'''
	Solve combinations and permutations.

	n is either n or all arguments depending of the for they're
	written in

	combinations and permutations written
	both as C(5, 2) and 5C2 evaluated as: 5 choose 2
	if written as mCn it will only take numbers not expressions
	unless parentheses are used. In order of operations nCm comes
	first.
	Combinations and permutations both used the gamma function
	in place of factorials and as a result will take
	non-integer arguments
	'''

	if form == "choose":  # if written as nCm

		if m is None:
			raise CalculatorError(
				"combinations_and_permutations requires a fourth "
				"argument when using choose notation")

		# turn the arguments into floats and give them more
		# descriptive names
		inner_n = float(n)
		inner_m = float(m)

		# find permutations
		temp_result = math.gamma(1 + inner_n) \
			/ math.gamma(1 + inner_n - inner_m)

		# if combinations also divide by m!
		if letter == "C":
			temp_result = temp_result / math.gamma(1 + inner_m)
		elif letter == "P":
			pass
		else:
			raise CalculatorError(
				"Second argument must be 'C' or 'P'"
				" for combinations or permutations not '%s'" % letter)

		return str(temp_result)

	elif form == "func":  # if written as C(5, 2)
		if m:
			raise CalculatorError(
				"combinations_and_permutations can not take a fourth "
				"argument when using function notation")

		# find the arguments of the function and cut off
		# everything else
		# sin(C(5, 2)) ← the last parenthesis
		proto_inner = find_match(n)

		# remove outer parentheses
		x = proto_inner[0][1:-1]

		# separate the arguments
		comb_args = separate(x)
		if len(comb_args) != 2:
			raise CalculatorError(
				"combinations_and_permutations takes exactly "
				"two arguments %s were provided." % len(comb_args))

		# evaluate each of the arguments separately
		inner_n = float(simplify(comb_args[0]))
		inner_m = float(simplify(comb_args[1]))

		# find permutations
		temp_result = math.gamma(1 + inner_n) \
			/ math.gamma(1 + inner_n - inner_m)

		# if combinations also divide by m!
		if letter == "C":
			temp_result = temp_result / math.gamma(1 + inner_m)
		elif letter == "P":
			pass
		else:
			raise CalculatorError(
				"Second argument must be 'C' or 'P'"
				" for combinations or permutations not '%s'" % letter)

		# add on anything that was was cut off the end when finding
		# the arguments
		# sin(C(5, 2)) ← the last parenthesis
		return str(temp_result) + proto_inner[1]
	else:
		raise CalculatorError(
			"First argument must be 'choose' or "
			"'func' not '%s'" % form)


def statistics_functions(function, args):
	'''
	Perform general statistics functions.

	This may in the future include any function that
	can have an arbitrarily large number of arguments.
	'''

	# find the arguments of the function and cut off
	# everything else
	# sin(mean(4, 2)) ← the last parenthesis
	proto_inner = find_match(args)

	# separate the arguments based on commas that are not
	# within more than one set of parentheses
	ave_args = separate(proto_inner[0][1:-1])

	try:
		# evaluate all the arguments
		list_ave = list(map((lambda x: float(simplify(x))), ave_args))
	except ValueError as e:
		raise CalculatorError(str(e))

	# perform the different functions
	if function.lower() in ("ave", "average", "mean"):
		result = stats.mean(list_ave)
	elif function.lower() == "median":
		result = stats.median(list_ave)
	elif function.lower() == "mode":
		result = stats.mode(list_ave)
	elif function.lower() == "max":
		result = max(list_ave)
	elif function.lower() == "min":
		result = min(list_ave)
	# this is the sample standard deviation
	elif function.lower() in ("stdev"):
		result = stats.stdev(list_ave)
	else:
		raise CalculatorError(
			"'%s' is not a function that is defined in"
			" statistics_functions" % function)

	# add on anything that was was cut off the end when finding
	# the arguments
	# sin(mean(4, 2)) ← the last parenthesis
	return float_to_str(result) + proto_inner[1]


def single_argument(func, args):
	'''
	Evaluate trig functions and other unary operators.
	'''

	global degree_mode

	if check_if_ascii(func):
		func = func.lower()

	# find the arguments of the function and cut off
	# everything else
	# tan(sin(π)) ← the last parenthesis when
	# evaluating sin
	proto_inner = find_match(args)
	proto_inner = list(proto_inner)

	# looks for the degree symbol in the argument
	# if the program finds it degree mode is set to true
	# for the particular operation
	if "°" in proto_inner[0]:
		if degree_mode == 0:
			degree_mode = 1
		proto_inner[0] = re.sub(
			"[°]",
			"",
			proto_inner[0],
			flags = re.I)

	# evaluate the argument into a form that math.log
	# can accept
	pre_inner = simplify(proto_inner[0])
	try:
		inner = float(pre_inner)
	except ValueError as e:
		raise CalculatorError(str(e))

	# check if in degree mode and if its doing an
	# operation that takes an angle as an argument
	if degree_mode > 0 and "in" in one_arg_funcs[func][1]:
		inner = math.pi * inner / 180

	result = one_arg_funcs[func][0](inner)

	# checks if its in degree mode (not because of
	# degree symbols in the argument) and if so
	# converts the answer to degrees for functions that
	# output an angle
	if degree_mode == 2 and "out" in one_arg_funcs[func][1]:
		result = result * 180 / math.pi

	# resets the degree mode for the session
	if degree_mode == 1:
		degree_mode = 0

	# this is a fix for the output being in
	# scientific notation and the program mistaking the
	# e for the constant e
	try:
		result = float_to_str(result)
	except (ValueError, TypeError):
		pass

	# add back anything that was cut off when finding the
	# argument of the inner function
	# tan(sin(π)) ← the last parenthesis when
	# evaluating sin
	return result + proto_inner[1]


def factorial(arg):
	'''
	Evaluate factorials.

	Interprets x! mathematically as gamma(x + 1)
	if written with an "!" will only take numbers as an argument.
	In order of operations factorials come after exponents,
	but before modulus

	>>> factorial("5")
	120.0
	'''

	return math.gamma(float(arg) + 1)


def logarithm(log_arg):
	'''
	Solve logarithms.

	Can be written log(a, b) or ln(x). Ln only takes one argument
	and is evaluated separately from log.
	'''

	# find the arguments of the function and cut off
	# everything else
	# sin(log(4, 2)) ← the last parenthesis
	proto_inner = find_match(log_arg)

	# separate the arguments based on commas that are not
	# within more than one set of parentheses
	log_args = separate(proto_inner[0][1:-1])

	if len(log_args) == 2:  # if written as log(a, b)

		# evaluate the arguments individually into a form
		# that math.log can accept
		argument = float(simplify(log_args[0]))
		base = float(simplify(log_args[1]))

		# perform the logarithm
		if base == 2:
			result = math.log2(argument)
		elif base == 10:
			result = math.log10(argument)
		elif base == math.e:
			result = math.log(argument)
		else:
			result = math.log(argument, base)

		return str(result) + proto_inner[1]

	elif len(log_args) == 1:  # if written as ln(x)

		result = math.log(float(simplify(proto_inner[0])))

	else:
		raise CalculatorError(
			"There must be 1 or 2 arguments in the "
			"input string")

	# add on anything that was was cut off the end when finding
	# the arguments
	# sin(log(4, 2)) ← the last parenthesis
	return str(result) + proto_inner[1]


def modulus(arg):
	'''
	Find the modulus of the input as a function not an operator.

	>>> modulus("(8, 4)")
	'0.0'

	>>> modulus("(7, 4)")
	'3.0'
	'''

	# find the arguments of the function and cut off
	# everything else
	# sin(mod(5, 2)) ← the last parenthesis
	proto_inner = find_match(arg)

	# separate the arguments based on commas that are not
	# within more than one set of parentheses
	mod_args = separate(proto_inner[0][1:-1])

	if len(mod_args) != 2:
		raise CalculatorError(
			"mod takes exactly two arguments %s were"
			" given." % len(mod_args))

	# evaluate the arguments individually into a form that fmod
	# can accept
	inner1 = float(simplify(mod_args[0]))
	inner2 = float(simplify(mod_args[1]))

	# do the actual modulation
	result = math.fmod(inner1, inner2)

	# add on anything that was was cut off the end when finding
	# the arguments
	# sin(mod(5, 2)) ← the last parenthesis
	return str(result) + proto_inner[1]


def abs_value(input):
	'''
	Break up a expression based on where pipes are and return the
	the absolute value of what is in them. Only does the first inner
	most layer, does not necessarily output a single number.

	>>> abs_value("|3-|2-4||")
	'|3-2.0|'

	>>> abs_value("|1-2|+|3-1|")
	'1.0+|3-1|'
	'''

	parts = input.split("|")

	if len(parts) % 2 == 0:
		raise CalculatorError(
			"There must be an even number of pipes in an "
			"absolute value expression.")

	for i in range(len(parts)):
		if parts[i].startswith(("+", "*", "^", "/")) or\
			parts[i].endswith(("+", "*", "^", "/", "-")) or\
			not parts[i]:
			pass

		else:
			result = math.fabs(float(simplify(parts[i])))
			last = ""
			iter_last = []
			next = ""
			iter_next = []

			if i > 0:
				last = parts[i - 1]
				if i > 1:
					iter_last = parts[:i - 1]

			if i < len(parts) - 1:
				next = parts[i + 1]
				if i < len(parts) - 2:
					iter_next = parts[i + 2:]

			result = last + str(result) + next
			result = "|".join(iter_last + [result] + iter_next)

			return result


def comma(left, right):
	'''
	Concatenate numbers separated by commas.

	Will raise CalculatorError if commas are not separating the
	integer portion of the number every three digits starting at the
	decimal point.

	>>> comma("3", "111.2")
	'3111.2'
	'''

	if "." not in right:
		if left.isdigit() and len(right) == 3 and\
			right.isdigit():
			return left + right
		else:
			raise CalculatorError(
				"Commas used inappropriately.")
	else:
		parts = right.split(".")
		if left.isdigit() and len(parts[0]) == 3 and\
			(parts[1].isdigit() or parts[1] == ""):
			return left + right
		else:
			raise CalculatorError(
				"Commas used inappropriately.")


# main func
def simplify(s):
	'''
	Simplify an expression.

	This is the main body of the program.

	>>> simplify("5--2")
	'7'
	'''

	global degree_mode

	original = s

	logger.debug("simplify is starting with the value '%s'" % s)

	# iterates over all the operations
	for key, value in regular_expr.items():

		# solution to scientific notation being mistaken
		# for the constant e
		if key == "const_comp":
			try:
				s = float_to_str(s)
			except (ValueError, TypeError):
				pass

		# checks for the operation
		m = re.search(value, s)

		# continues until all instances of an
		# operation have been dealt with
		while m is not None:

			logger.debug(
				"'{match}' was matched by '{key}' in '{s}'".format(
					match = m.groups(), key = key, s = s))

			if key == "command_comp":
				# non-math commands

				# display history
				if m.group(1) is not None:
					print(history[-1 * hist_len:])

				# exit the program
				elif m.group(2) is not None:
					sys.exit()

				# set degree mode on for the session
				elif m.group(3) is not None:
					switch_degree_mode(2)

				# set degree mode off for the session
				elif m.group(4) is not None:
					switch_degree_mode(0)

				else:
					raise CalculatorError(
						"Command must be 'history',"
						" 'exit', 'quit', 'degree mode', or 'radian "
						"mode'.")

				return None

			elif key == "implicet_mult_pre_const_comp":

				result = m.group(1) + "*"

			elif key == "const_comp":

				result = constant(m.group(1))

			elif key == "implicet_mult_comp":

				if m.group(1):
					result = m.group(1) + "*"
				elif m.group(2):
					result = m.group(2)[0] + "*" + m.group(2)[1]
				else:
					raise CalculatorError(
					"Implicit multiplication was found but neither "
					"group was matched.")

			elif key == "graph_comp":

				graph_out = graph_function(m.group(1))
				return "Done"

			elif key == "alg_comp":

				result = solve_equations(m.group(1))

			elif key == "eval_comp":

				result = evaluate(m.group(1), m.group(2))

			elif key == "der_comp":

				if m.group(3) is not None:
					result = find_derivative(
						m.group(1), m.group(2),
						var = m.group(3)[-1])
				else:
					result = find_derivative(m.group(1), m.group(2))

			elif key == "int_comp":

				result = integrate_function(
					m.group(1), m.group(2),
					m.group(3), m.group(4))

			elif key == "conv_comp":
				result = convert(m.group(1), m.group(2), m.group(3))

			elif key == "comb_comp":
					result = combinations_and_permutations(
						"func",
						m.group(1),
						m.group(2))
			elif key == "choose_comp":
					result = combinations_and_permutations(
						"choose",
						m.group(2),
						m.group(1),
						m.group(3))

			elif key == "ave_comp":

				result = statistics_functions(m.group(1), m.group(2))

			elif key == "trig_comp":

				result = single_argument(m.group(1), m.group(2))

			elif key == "fact_comp":

				result = factorial(m.group(1))

			elif key == "log_comp":

				result = logarithm(m.group(1) or m.group(2))

			elif key == "abs_comp":

				result = abs_value(s)

			elif key == "paren_comp":

				# recursively evaluates the innermost parentheses
				result = simplify(m.group(1))

			elif key == "comma_comp":

				# just concatenates whats on either side
				# of the parentheses unless its separating
				# arguments of a function

				result = comma(m.group(1), m.group(2))

			elif key == "exp_comp":

				result = float(m.group(1)) ** float(m.group(3))

			elif key in ("mod_comp", "mod2_comp"):

				# modulus written as both mod(x, y) and x % y
				# where x is the dividend and y is the divisor
				# if written as x % y it will only take numbers
				# for arguments. In order of operations modulus comes
				# after exponents and factorials, but before
				# multiplication and division

				if key == "mod2_comp":

					result = modulus(m.group(1))

				elif key == "mod_comp":

					# the x % y format
					result = math.fmod(
						float(m.group(1)),
						float(m.group(2)))

				else:
					raise CalculatorError(
						"How could this possibly "
						"happen? It just tested if i was 'mod2_comp' "
						"or 'mod_comp'.")

			elif key == "per_comp":

				# percentage signs act just like dividing by 100
				result = "/100"

			elif key == "mult_comp":

				# multiplication and division

				if m.group(2) == "*":

					result = float(m.group(1)) * float(m.group(3))

				elif m.group(2) in ("/", "÷"):

					result = float(m.group(1)) / float(m.group(3))

				else:
					raise CalculatorError(
						"mult_comp must match '*', "
						"'//', or '÷'.")

			elif key == "add_comp":

				# addition and subtraction

				if m.group(2) == "+":

					result = math.fsum((
						float(m.group(1)),
						float(m.group(3))))

				elif m.group(2) == "-":

					result = float(m.group(1)) - float(m.group(3))

				else:
					raise CalculatorError(
						"add_comp must match '+' or '-'.")
			
			elif key == "assign_comp":
				
				# variable assigment
				
				global constant_dict
				
				constant_dict[m.group(1)] = simplify(m.group(2))
				
				result = "Done"
				

			else:
				raise CalculatorError(
					"Function: '%s' not implemented." % key)

			if key not in (
				"command_comp", "const_comp",
				"alg_comp", "eval_comp", "der_comp"):

				# this is a fix for python returning
				# answers in scientific notation which since
				# it has e it mistakes the constant e
				try:
					result = float_to_str(result)
				except (ValueError, TypeError):
					pass

			# replace the text matched by i (the regular expression)
			# with the result of the mathematical expression
			s = re.sub(value, str(result), s, count = 1)
			logger.debug(
				"'{result}' has has been substituted into "
				"'{original}' resulting in '{new}'".format(
					result = result, original = original, new = s))

			m = re.search(value, s)
	try:
		s = float_to_str(s)
	except (ValueError, TypeError):
		pass
	return s


# pre and post processing for console
def ask(s = None):
	'''
	Ask the user what expression they want to simplify
	and do pre and post processing when using the console.
	'''

	global ans
	if s is None:

		# get input from the user
		s = input("input an expression: ")

		# add the user input to the history
		history.append(s)

		# save history to file
		save_info(history = history)

	try:
		# evaluate the expression
		out = simplify(s)
	except CalculatorError as e:
		print(s, " failed: ", e)
		logger.error(s + " failed: " + str(e))

	else:
		# save output to be used by the user
		ans = out

		# display the output
		if out is not None:
			print(s + " = " + out)
		print("")

		# save answer to file to be used next session
		save_info(ans = ans)


def key_pressed(event):
	'''
	Handle keys pressed in the GUI.

	Used keys are the up arrow, down arrow, the enter key, and
	backspace.
	'''

	global up_hist, input_widget

	try:
		code = event.keycode
	except AttributeError:
		code = event

	if code in key_binds[os.name]:
		key = key_binds[os.name][code]
	else:
		key = None
	#print(code)

	if key == "enter":
		get_input()

	elif key == "backspace":
		pass
		#out = input_backspace()
		#if out is not None:
		#	return out

	# go backwards in the history when the up arrow is pressed
	elif key == "up":
		if up_hist < len(history):
			up_hist += 1
			input_widget.delete(0, "end")
			input_widget.insert(0, history[-1 * up_hist])

	# go forwards in the history when the down arrow is pressed
	elif key == "down":
		if up_hist > 1:
			up_hist -= 1
			input_widget.delete(0, "end")
			input_widget.insert(0, history[-1 * up_hist])

	# if you are not navigating the history stop keeping
	# track of where you are
	if key not in ("up", "down"):
		up_hist = 0


def input_backspace(*event):
	'''
	Delete the last character in the entry widget.
	'''

	global input_widget

	delete_chr_comp = compile_ignore_case(
		"^(.*?)(" + "\(|".join(list_functions) + ")?$")

	a = input_widget.get()
	cursor_pos = input_widget.index("insert")

	fm = re.search(delete_chr_comp, a[:cursor_pos])

	if fm.group(2) is None:
		input_widget.delete(0, "end")
		input_widget.insert(0, a[:cursor_pos - 1] + a[cursor_pos:])
		input_widget.icursor(cursor_pos - 1)
	else:
		input_widget.delete(0, "end")
		input_widget.insert(0, fm.group(1) + a[cursor_pos:])
		input_widget.icursor(cursor_pos - len(fm.group(2)))
		return "break"


def get_input(s = None):
	'''
	Get user input from the entry widget.
	'''

	global ans, mess

	if s is None:
		pre_s = input_widget.get()
		if pre_s != "":
			s = pre_s

	if s == "":
		if os.name == "posix":
			exit()
		elif os.name == "nt":
			sys.exit()

	if s is not None:

		# add the user input to the history
		history.append(s)

		# save history to file
		save_info(history = history)

		try:
			out = simplify(s)
		except CalculatorError as e:
			mess.set(s + " failed: " + str(e))
			logger.error(s + " failed: " + str(e))
		else:
			# save output to be used by the user
			ans = out

			# display the output
			if out is not None:
				mess.set(s + " = " + out)

			# save answer to file to be used next session
			save_info(ans = ans)

		# clear the input box
		input_widget.delete(0, "end")


def switch_trig():
	'''
	Put the trig function buttons on the GUI.

	Remove the hyperbolic, miscellaneous, and statistics function
	buttons then use grid to place the trig function buttons.
	'''

	# remove the buttons for the hyperbolic functions, misc functions,
	# and stats functions
	for i in range(12):
		hyperbolic_func_buttons[i].grid_forget()
		try:
			misc_func_buttons[i].grid_forget()
		except IndexError:
			pass
		try:
			stats_func_buttons[i].grid_forget()
		except IndexError:
			pass

	for i in range(12):
		trig_func_buttons[i].grid(row = i // 3 + 3, column = i % 3 + 8)


def switch_hyperbolic():
	'''
	Put the hyperbolic function buttons in the GUI.

	Remove the trig, miscellaneous, and statistics function buttons
	if present then use grid to place the hyperbolic function buttons.
	'''

	# remove the buttons for the trig functions, misc functions,
	# and stats functions
	for i in range(12):
		trig_func_buttons[i].grid_forget()
		try:
			misc_func_buttons[i].grid_forget()
		except IndexError:
			pass
		try:
			stats_func_buttons[i].grid_forget()
		except IndexError:
			pass

	for i in range(12):
		hyperbolic_func_buttons[i].grid(
			row = i // 3 + 3,
			column = i % 3 + 8)


def switch_misc():
	'''
	Put the miscellaneous function buttons on the GUI.

	Remove the trig, hyperbolic, and statistics buttons if they
	are present then use grid place the miscellaneous function buttons.
	'''

	# remove the buttons for the trig functions, hyperbolic functions,
	# and stats functions
	for i in range(12):
		trig_func_buttons[i].grid_forget()
		hyperbolic_func_buttons[i].grid_forget()
		try:
			stats_func_buttons[i].grid_forget()
		except IndexError:
			pass

	for i in range(10):
		misc_func_buttons[i].grid(row = i // 3 + 3, column = i % 3 + 8)


def switch_stats():
	'''
	Put the statistics function buttons in the GUI.

	Remove the trig, hyperbolic, and misc function buttons if
	present then use grid to place the statistics function buttons.
	'''

	# remove the buttons for the trig functions, misc functions,
	# and hyperbolic functions
	for i in range(12):
		trig_func_buttons[i].grid_forget()
		hyperbolic_func_buttons[i].grid_forget()
		try:
			misc_func_buttons[i].grid_forget()
		except IndexError:
			pass

	# mean median mode
	for i in range(6):
		stats_func_buttons[i].grid(
			row = i // 3 + 3,
			column = i % 3 + 8)


def format_default_screen(menubar):
	'''
	Put the buttons in place on the GUI.

	Use grid to place the buttons for the digits 0-10, a decimal point,
	plus, minus, multiply, divide, exponents, factorial, pi, e,
	parentheses, absolute value pipes, comma, integral, x, the enter
	key, backspace, and the menu to switch between function sets. Then
	call switch_trig to place the trig function buttons.
	'''

	# 7 8 9
	digit_button[7].grid(row = 3, column = 0)
	digit_button[8].grid(row = 3, column = 1)
	digit_button[9].grid(row = 3, column = 2)

	# 4 5 6
	digit_button[4].grid(row = 4, column = 0)
	digit_button[5].grid(row = 4, column = 1)
	digit_button[6].grid(row = 4, column = 2)

	# 1 2 3
	digit_button[1].grid(row = 5, column = 0)
	digit_button[2].grid(row = 5, column = 1)
	digit_button[3].grid(row = 5, column = 2)

	# 0 .
	digit_button[0].grid(row = 6, column = 0)
	digit_button[10].grid(row = 6, column = 1)  # .

	digit_button[11].grid(row = 3, column = 4)  # +
	digit_button[12].grid(row = 3, column = 5)  # -
	digit_button[13].grid(row = 4, column = 4)  # *
	digit_button[14].grid(row = 4, column = 5)  # ÷
	digit_button[15].grid(row = 5, column = 4)  # ^
	digit_button[16].grid(row = 5, column = 5)  # !
	digit_button[17].grid(row = 6, column = 4)  # π
	digit_button[18].grid(row = 6, column = 5)  # e
	digit_button[19].grid(row = 3, column = 6)  # (
	digit_button[20].grid(row = 3, column = 7)  # )
	digit_button[21].grid(row = 4, column = 6)  # |
	digit_button[22].grid(row = 4, column = 7)  # ,
	digit_button[23].grid(row = 5, column = 6)  # ∫
	digit_button[24].grid(row = 5, column = 7)  # x

	equals_button.grid(row = 6, column = 2)  # =
	back_button.grid(row = 3, column = 12)  # backspace

	# the functions menubutton
	menubar.grid(row = 3, column = 11)

	switch_trig()


def switch_matrices():
	'''
	Create window for dealing with matrices. NotImplemented.
	'''

	pass


def graph_win_key_press(event, index):
	'''
	Deal with key presses while editing the graph window.

	The up arrow will move the cursor to the box above unless
	it is already in the top box. The down arrow will move the
	cursor into the box below it unless it is already in the
	bottom box.
	'''

	global g_bound_entry

	try:
		code = event.keycode
	except AttributeError:
		code = event

	if code in key_binds[os.name]:
		if key_binds[os.name][code] == "up" and index > 0:
			g_bound_entry[g_bound_names[index - 1]].focus()
		elif key_binds[os.name][code] == "down" and\
			index < len(g_bound_names) - 1:
			g_bound_entry[g_bound_names[index + 1]].focus()


def edit_graph_window():
	'''
	Create a window to change the graph window bounds.
	'''

	global g_bound_entry, g_bound_string

	root = tk.Toplevel()

	g_bound_entry = {}
	g_bound_string = {}
	g_bound_disp = {}
	for index, val in enumerate(g_bound_names):
		g_bound_entry[val] = tk.Entry(root)

		g_bound_entry[val].grid(row = index, column = 1)

		g_bound_string[val] = tk.StringVar()
		g_bound_string[val].set("%s = %s" % (val, win_bound[val]))

		g_bound_disp[val] = tk.Message(
			root,
			textvariable = g_bound_string[val],
			width = 100)

		g_bound_disp[val].grid(row = index, column = 0)

		g_bound_entry[val].bind(
			"<Key>",
			lambda event, i = index: graph_win_key_press(event, i))

	root.bind("<Return>", lambda a: change_graph_win_set())

	root.mainloop()


def tkask(s = None):
	'''
	Make a GUI for the program.

	Create instances of all the buttons that may be needed and
	call format_default_screen to place the digits and other
	buttons that don't change.
	'''

	global input_widget, mess
	global digit_button, equals_button, back_button
	global trig_func_buttons, inverse_trig_func_buttons
	global hyperbolic_func_buttons, inverse_hyperbolic_func_buttons
	global misc_func_buttons, stats_func_buttons

	root = tk.Tk()

	root.title("ReCalc")

	if os.name == "nt" and os.path.isfile(
		os.path.join(calc_path, "ReCalc_icon.ico")):
		root.iconbitmap(default = os.path.join(
			calc_path,
			"ReCalc_icon.ico"))

	mess = tk.StringVar()
	mess.set("Input an expression")

	# output text widget
	output_mess_widget = tk.Message(
		root,
		textvariable = mess,
		width = 200)
	output_mess_widget.grid(row = 0, column = 0, columnspan = 11)

	# input text widget
	input_widget = tk.Entry(root, width = 90)
	input_widget.grid(row = 1, column = 0, columnspan = 12)
	input_widget.focus()

	# list of basic buttons
	button_keys = list(range(10)) + [
		".", "+", "-", "*", "÷", "^", "!", "π", "e", "(", ")", "|",
		",", "∫", "x"]

	# creating of the basic buttons
	digit_button = list(tk.Button(
		root,
		text = str(i),
		command = lambda k = i: input_widget.insert(
			input_widget.index("insert"), k),
		width = 5) for i in button_keys)

	# equals button
	equals_button = tk.Button(
		root,
		text = "=",
		command = get_input,
		width = 5,
		bg = "light blue")

	# backspace button
	back_button = tk.Button(
		root,
		text = "delete",
		command = input_backspace,
		width = 5)

	# list of trig functions
	trig_funcs = (
		"sin(", "cos(", "tan(",
		"sec(", "csc(", "cot(",
		"arcsin(", "arccos(", "arctan(",
		"arcsec(", "arccsc(", "arccot(")

	# creating of trig function buttons
	trig_func_buttons = list(tk.Button(
		root,
		text = i[:-1],
		command = lambda k = i: input_widget.insert(
			input_widget.index("insert"), k),
		width = 5) for i in trig_funcs)

	# list of hyperbolic functions
	hyperbolic_funcs = (
		"sinh(", "cosh(", "tanh(",
		"sech(", "csch(", "coth(",
		"arcsinh(", "arccosh(", "arctanh(",
		"arcsech(", "arccsch(", "arccoth(")

	# creation of hyperbolic function buttons
	hyperbolic_func_buttons = list(tk.Button(
		root,
		text = i[:-1],
		command = lambda k = i: input_widget.insert(
			input_widget.index("insert"), k),
		width = 5) for i in hyperbolic_funcs)

	# list of misc fuctions
	misc_funcs = (
		"log(", "ln(", "Γ(", "abs(", "ceil(", "floor(",
		"erf(", "mod(", "C(", "P(")

	# creation of misc function buttons
	misc_func_buttons = list(tk.Button(
		root,
		text = i[:-1],
		command = lambda k = i: input_widget.insert(
			input_widget.index("insert"), k),
		width = 5) for i in misc_funcs)

	# list of stats functions
	stats_funcs = (
		"mean(", "median(", "mode(", "stdev(", "max(", "min(")

	# creation of stats buttons
	stats_func_buttons = list(tk.Button(
		root,
		text = i[:-1],
		command = lambda k = i: input_widget.insert(
			input_widget.index("insert"), k),
		width = 5) for i in stats_funcs)

	# more functions button
	menubar = tk.Menubutton(
		root,
		text = "Functions",
		relief = "raised")
	dropdown = tk.Menu(menubar, tearoff = 0)
	dropdown.add_command(
		label = "Trig Functions",
		command = switch_trig)
	dropdown.add_command(
		label = "Hyperbolic Functions",
		command = switch_hyperbolic)
	dropdown.add_command(
		label = "Stats Functions",
		command = switch_stats)
	dropdown.add_command(
		label = "Misc Functions",
		command = switch_misc)

	menubar.config(menu = dropdown)

	# menu at top right of screen
	options_menu = tk.Menu(root)
	list_options = tk.Menu(options_menu, tearoff = 0)

	list_options.add_command(
		label = "Radian Mode",
		command = lambda: switch_degree_mode("radian"))

	list_options.add_command(
		label = "Degree Mode",
		command = lambda: switch_degree_mode("degree"))

	list_options.add_command(
		label = "Polar Mode",
		command = lambda: switch_polar_mode("polar"))

	list_options.add_command(
		label = "Cartesian Mode",
		command = lambda: switch_polar_mode("Cartesian"))

	list_options.add_command(
		label = "Parametic Mode",
		command = lambda: switch_polar_mode("parametric"))

	list_options.add_command(
		label = "Change length of history print back",
		command = change_hist_len_win)

	list_options.add_command(
		label = "Change der approx",
		command = change_der_approx_win)

	list_options.add_command(
		label = "Delete history",
		command = delete_history)

	options_menu.add_cascade(label = "Options", menu = list_options)

	# list of other things the calculator can do
	matrices_plus = tk.Menu(options_menu, tearoff = 0)
	matrices_plus.add_command(
		label = "Matrices",
		command = switch_matrices)
	matrices_plus.add_command(
		label = "Window",
		command = edit_graph_window)
	options_menu.add_cascade(label = "Things", menu = matrices_plus)

	root.config(menu = options_menu)

	format_default_screen(menubar)

	root.bind("<Key>", key_pressed)

	get_input(s = s)

	root.mainloop()


def main():
	'''
	Handle command line arguments and decide whether or not to use
	the GUI.
	'''

	global logger, use_gui

	if "docopt" in sys.modules:
		args = docopt(__doc__)
		
		if args["-V"] or args["--version"]:
			print(version)
			sys.exit()
		if args["-c"] or args["--commandline"]:
			use_gui = False
		if args["-v"] or args["--verbose"]:
			logger.setLevel(logging.DEBUG)
		start_exp = " ".join(args["EXPRESSION"])

		if start_exp == "":
			start_exp = None
	else:
		start_exp = None

	# default startup
	if "tkinter" in sys.modules and use_gui:
		tkask(start_exp)
	else:
		ask(start_exp)
		while True:
			ask()


if __name__ == "__main__":
	main()
