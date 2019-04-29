"""
***************************
compas_fofin.datastructures
***************************

.. currentmodule:: compas_fofin.datastructures


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Shell


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    shell_update_xyz_numpy
    shell_update_xyz_numpy_proxy

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from .shell import *
from .shell_equilibrium_numpy import *


__all__ = [name for name in dir() if not name.startswith('_')]
