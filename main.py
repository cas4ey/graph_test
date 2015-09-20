# coding=utf-8
#!/usr/bin/env python
# -----------------
# file      : main.py
# date      : 2015/05/19
# author    : Victor Zarubkin
# contact   : victor.zarubkin@gmail.com
# copyright : Copyright (C) 2015  Victor Zarubkin
# license   : This file is part of GraphTutorial.
#           :
#           : GraphTutorial is free software: you can redistribute it and/or modify
#           : it under the terms of the GNU General Public License as published by
#           : the Free Software Foundation, either version 3 of the License, or
#           : (at your option) any later version.
#           :
#           : GraphTutorial is distributed in the hope that it will be useful,
#           : but WITHOUT ANY WARRANTY; without even the implied warranty of
#           : MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#           : GNU General Public License for more details.
#           :
#           : You should have received a copy of the GNU General Public License
#           : along with BehaviorStudio. If not, see <http://www.gnu.org/licenses/>.
#           :
#           : A copy of the GNU General Public License can be found in file COPYING.
############################################################################

"""

"""

__author__ = 'Victor Zarubkin'
__copyright__ = 'Copyright (C) 2015  Victor Zarubkin'
__credits__ = ['Victor Zarubkin']
__license__ = ['GPLv3']
__version__ = '0.0.1'  # this is last application version when this script file was changed
__email__ = 'victor.zarubkin@gmail.com'
############################################################################

import sys

from main_window import MainWindow
from PySide.QtGui import *
from quaternion import *
from math import radians, pi


def main(argv):
    # Create a Qt application
    app = QApplication(argv)
    app.setStyle('macintosh')

    window = MainWindow()
    window.show()

    # Enter Qt application main loop
    app.exec_()
    sys.exit()


def main2():
    axis = Vector3(1, 0, 0)
    angle = radians(90)
    q = Quaternion.from_axis_angle(axis, angle)
    v = Vector3(0, 1, 1)
    p = q * Quaternion.from_vector(v) * q.inverse()
    # print('cos(angle/2) = {0}'.format(cos(pi * 0.500000000000000000000000000000000000000000)))
    print('v = (x = {0}, y = {1}, z = {2})'.format(v.x, v.y, v.z))
    print('q = (x = {0}, y = {1}, z = {2}, w = {3})'.format(q.x, q.y, q.z, q.w))
    print('p = (x = {0}, y = {1}, z = {2}, w = {3})'.format(p.x, p.y, p.z, p.w))


if __name__ == '__main__':
    main(sys.argv)
    # main2()
