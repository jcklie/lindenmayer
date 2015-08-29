****************************************
lindenmayer: a CLI to generate fractals with L-Systems
****************************************

=============
Usage
=============

::

	Lindenmayer. Creates fractals from L-Systems.

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

=============
Installation
=============

=============
Examples
=============

--------------------------
Dragon curve with 13 iterations
--------------------------

.. image:: https://raw.githubusercontent.com/Rentier/lindenmayer/master/examples/dragon_13.png
    :align: center

--------------------------
Koch curve with 5 iterations
--------------------------

.. image:: https://raw.githubusercontent.com/Rentier/lindenmayer/master/examples/koch_5.png
    :align: center

--------------------------
Levi C curve with 13 iterations
--------------------------    

.. image:: https://raw.githubusercontent.com/Rentier/lindenmayer/master/examples/levic_13.png
    :align: center