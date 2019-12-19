from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_fofin.datastructures import Shell
from compas_fofin.fofin import shell_update_xyz_numpy

from compas_plotters import MeshPlotter


HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '../data/mesh.obj')

# load a mesh from an OBJ
shell = Shell.from_obj(FILE)

# set the anchors
shell.set_vertices_attribute('is_anchor', True, keys=list(shell.vertices_where({'vertex_degree': 2})))

# compute equilibrium
shell_update_xyz_numpy(shell)

# visualize
plotter = MeshPlotter(shell, figsize=(10, 7))
plotter.draw_vertices()
plotter.draw_edges()
plotter.draw_faces()
plotter.show()
