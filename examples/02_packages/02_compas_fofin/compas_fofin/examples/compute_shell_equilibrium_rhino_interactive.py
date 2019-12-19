from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_fofin.datastructures import Shell
from compas.rpc import Proxy

from compas_fofin.rhino import ShellArtist
from compas_fofin.rhino import ShellHelper


fofin = Proxy('compas_fofin.fofin')


HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '../data/mesh.obj')

# load a mesh from an OBJ
shell = Shell.from_obj(FILE)

shell.attributes['density'] = 0.0

# set the anchors
shell.set_vertices_attribute('is_anchor', True, keys=list(shell.vertices_where({'vertex_degree': 2})))

artist = ShellArtist(shell, layer="FoFin::Shell")


def draw():
    artist.clear_layer()
    artist.draw_vertices(color={key: (255, 0, 0) for key in shell.vertices_where({'is_anchor': True})})
    artist.draw_edges()
    artist.draw_faces()
    artist.redraw()


draw()

while True:
    keys = ShellHelper.select_vertices(shell)
    if not keys:
        break
    if ShellHelper.update_vertex_attributes(shell, keys):
        draw()


while True:
    keys = ShellHelper.select_edges(shell)
    if not keys:
        break
    if ShellHelper.update_edge_attributes(shell, keys):
        draw()


# compute equilibrium
shell.data = fofin.shell_update_xyz_numpy_proxy(shell.to_data())

# visualize
artist.clear_layer()
artist.draw_vertices(color={key: (255, 0, 0) for key in shell.vertices_where({'is_anchor': True})})
artist.draw_edges()
artist.draw_faces()
artist.draw_forces(scale=0.01)
artist.draw_reactions()
