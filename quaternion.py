# coding=utf-8
# -----------------
# file      : quaternion.py
# date      : 2015/06/20
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
#           : A copy of the GNU General Public License can be found in file LICENSE.
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

from math import sin, cos, acos, fabs, sqrt


class Vector3(object):

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __iadd__(self, v):
        self.x += v.x
        self.y += v.y
        self.z += v.z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __isub__(self, v):
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __imul__(self, num):
        self.x *= num
        self.y *= num
        self.z *= num

    def __mul__(self, num):
        return Vector3(self.x * num, self.y * num, self.z * num)

    def __itruediv__(self, num):
        self.__imul__(1.0 / num)

    def __truediv__(self, num):
        return self.__mul__(1.0 / num)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __len__(self):
        return sqrt(self.dot_product(self))

    def normalize(self):
        self.__itruediv__(self.__len__())

    def normalized(self):
        return self.__truediv__(self.__len__())


class Quaternion(object):

    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    @staticmethod
    def from_axis_angle(axis, angle):
        half_angle = angle * 0.5
        s = sin(half_angle)
        return Quaternion(axis.x * s, axis.y * s, axis.z * s, cos(half_angle))

    @staticmethod
    def from_vector(v, w=0.0):
        return Quaternion(v.x, v.y, v.z, w)

    def v(self):
        return Vector3(self.x, self.y, self.z)

    def angle(self):
        return acos(self.w) * 2.0

    def axis(self):
        return self.v() if fabs(self.w) > 0.9999 else self.v() / sin(acos(self.w))

    def __neg__(self):
        return Quaternion(-self.x, -self.y, -self.z, -self.w)

    def __iadd__(self, q):
        self.x += q.x
        self.y += q.y
        self.z += q.z
        self.w += q.w
        return self

    def __add__(self, q):
        return Quaternion(self.x + q.x, self.y + q.y, self.z + q.z, self.w + q.w)

    def __isub__(self, q):
        self.x -= q.x
        self.y -= q.y
        self.z -= q.z
        self.w -= q.w
        return self

    def __sub__(self, q):
        return Quaternion(self.x - q.x, self.y - q.y, self.z - q.z, self.w - q.w)

    def __imul__(self, q):
        if isinstance(q, Quaternion):
            x = q.w * self.x + self.w * q.x + (self.y * q.z - self.z * q.y)
            y = q.w * self.y + self.w * q.y + (self.z * q.x - self.x * q.z)
            z = q.w * self.z + self.w * q.z + (self.x * q.y - self.y * q.x)
            w = q.w * self.w - self.v().dot_product(q.v())
            self.x = x
            self.y = y
            self.z = z
            self.w = w
        else:
            self.x *= q
            self.y *= q
            self.z *= q
            self.w *= q
        return self

    def __mul__(self, q):
        if isinstance(q, Quaternion):
            x = q.w * self.x + self.w * q.x + (self.y * q.z - self.z * q.y)
            y = q.w * self.y + self.w * q.y + (self.z * q.x - self.x * q.z)
            z = q.w * self.z + self.w * q.z + (self.x * q.y - self.y * q.x)
            w = q.w * self.w - self.v().dot_product(q.v())
            return Quaternion(x, y, z, w)
        else:
            return Quaternion(self.x * q, self.y * q, self.z * q, self.w * q)

    def __itruediv__(self, num):
        return self.__imul__(1.0 / num)

    def __truediv__(self, num):
        return self.__mul__(1.0 / num)

    def dot_product(self, q):
        return self.x * q.x + self.y * q.y + self.z * q.z + self.w * q.w

    def norm(self):
        return self.dot_product(self)

    def __len__(self):
        return sqrt(self.norm())

    def magnitude(self):
        return self.__len__()

    def normalize(self):
        self.__itruediv__(self.__len__())

    def normalized(self):
        self.__truediv__(self.__len__())

    def transpose(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def transposed(self):
        return Quaternion(-self.x, -self.y, -self.z, self.w)

    def conjugate(self):
        return self.transposed()

    def invert(self):
        self.transpose()
        self.__itruediv__(self.norm())

    def inverse(self):
        return self.transposed().__itruediv__(self.norm())

    @staticmethod
    def identity():
        return Quaternion(0, 0, 0, 1)


def slerp(q, p, t):
    cos_omega = q.dotProduct(p)
    omega = acos(cos_omega)
    return (q * sin((1.0 - t) * omega) + p * sin(t * omega)) / sin(omega)
