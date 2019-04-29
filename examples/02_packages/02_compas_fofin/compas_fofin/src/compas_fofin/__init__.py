"""
********************************************************************************
compas_fofin
********************************************************************************

.. currentmodule:: compas_fofin


.. toctree::
    :maxdepth: 1

    compas_fofin.datastructures
    compas_fofin.fofin
    compas_fofin.rhino
    compas_fofin.utilities


"""

from __future__ import print_function

import os
import sys

import compas


__author__ = ['tom van mele <van.mele@arch.ethz.ch>']
__copyright__ = 'Block Research Group - ETH Zurich'
__license__ = 'MIT License'
__email__ = 'van.mele@arch.ethz.ch'
__version__ = '0.1.0'


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, '../../'))
DATA = os.path.abspath(os.path.join(HOME, 'data'))
DOCS = os.path.abspath(os.path.join(HOME, 'docs'))
TEMP = os.path.abspath(os.path.join(HOME, 'temp'))


def get(filename):
    """Get the full path to one of the sample data files.

    Parameters
    ----------
    filename : str
        The name of the data file.
        The following are available.

        * boxes.obj
        * faces.obj
        * fink.obj
        * hypar.obj
        * lines.obj
        * saddle.obj

    Returns
    -------
    str
        The full path to the specified file.

    Notes
    -----
    The file name should be specified relative to the **COMPAS** sample data folder.
    This folder is only locally available if you installed **COMPAS** from source,
    or if you are working directly with the source.
    In all other cases, the function will get the corresponding files direcly from
    the GitHub repo, at https://raw.githubusercontent.com/compas-dev/compas/master/data

    Examples
    --------
    The ``compas.get`` function is meant to be used in combination with the static
    constructors of the data structures.

    .. code-block:: python

        import compas
        from compas.datastructures import Mesh

        mesh = Mesh.from_obj(compas.get('faces.obj'))

    """
    filename = filename.strip('/')

    localpath = compas._os.absjoin(DATA, filename)

    if os.path.exists(localpath):
        return localpath


__all__ = ['HOME', 'DATA', 'DOCS', 'TEMP']
