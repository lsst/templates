# 
# LSST Data Management System
#
# Copyright 2008-2017  AURA/LSST.
# 
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the LSST License Statement and 
# the GNU General Public License along with this program.  If not, 
# see <https://www.lsstcorp.org/LegalNotices/>.
#

from __future__ import absolute_import
import numpy as np

from lsst.utils import TemplateMeta
from .exampleThree import ExampleThreeF, ExampleThreeD

__all__ = [] # import for side effects

class ExampleThree(metaclass=TemplateMeta):
    pass

ExampleThree.register(np.float32, ExampleThreeF)
ExampleThree.register(np.float64, ExampleThreeD)
ExampleThree.alias("F", ExampleThreeF)
ExampleThree.alias("D", ExampleThreeD)

