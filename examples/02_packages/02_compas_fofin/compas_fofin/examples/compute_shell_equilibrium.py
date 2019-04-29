from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_fofin

from compas_fofin.datastructures import Shell
from compas_fofin.datastructures import shell_update_xyz_numpy

from compas.plotters import MeshPlotter


shell = Shell.from_obj(compas_fofin.get('mesh.obj'))

shell.set_vertices_attribute('is_anchor', True, keys=list(shell.vertices_where({'vertex_degree': 2})))

shell_update_xyz_numpy(shell)

plotter = MeshPlotter(shell)

plotter.draw_vertices()
plotter.draw_edges()
plotter.draw_faces()

plotter.show()
