from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
from compas.datastructures import Mesh
from compas.datastructures import mesh_split_edge
from compas.geometry import normalize_vector
from compas.geometry import centroid_points


__all__ = ['Shell']


class Shell(Mesh):
    """The ``Shell`` data structure extends the ``Mesh`` half-edge data structure."""

    def __init__(self):
        super(Shell, self).__init__()
        self.attributes.update({
            'color.vertex'            : (0, 0, 0),
            'color.face'              : (255, 255, 255),
            'color.edge'              : (0, 0, 0),
            'color.force:compression' : (255, 0, 0),
            'color.force:tension'     : (255, 0, 0),
            'color.reaction'          : (0, 255, 0),
            'color.residual'          : (0, 255, 255),
            'color.load'              : (0, 0, 255),
            'color.selfweight'        : (255, 255, 255),
            'color.normal:vertex'     : (0, 255, 0),
            'color.normal:face'       : (0, 255, 0),
            'scale.force'             : 0.1,
            'scale.stress'            : 0.1,
            'scale.reaction'          : 1.0,
            'scale.residual'          : 1.0,
            'scale.load'              : 1.0,
            'scale.selfweight'        : 1.0,
            'tol.reaction'            : 1e-3,
            'tol.residual'            : 1e-3,
            'tol.force'               : 1e-3,
            'tol.stress'              : 1e-3,

            'density' : 14,
        })
        self.update_default_vertex_attributes({
            'rx' : 0.0,
            'ry' : 0.0,
            'rz' : 0.0,
            'px' : 0.0,
            'py' : 0.0,
            'pz' : 0.0,
            't'  : 1.0,
            'nx' : None,
            'ny' : None,
            'nz' : None,
            'is_anchor' : False,
            'is_fixed'  : False,
            'constraint': None,
            'param'     : None,
        })
        self.update_default_edge_attributes({
            'q'  : 1.0,
            'f'  : 0.0,
            'l'  : 0.0,
            'l0' : 0.0,
            'E'  : 0.0,
            'r'  : 0.0,
            'is_edge' : True,
        })
        self.update_default_face_attributes({
            'zone' : 0
        })

    @property
    def layer(self):
        """str : The name of the layer.

        Any value assigned to this property will be stored in the attribute dict
        of the data structure instance.
        """
        return self.attributes['layer'] or self.name

    @layer.setter
    def layer(self, value):
        self.attributes['layer'] = value

    @classmethod
    def from_rhinomesh(cls, guid):
        from compas_rhino.helpers import mesh_from_guid
        return mesh_from_guid(cls, guid)

    def get_continuous_edges(self, uv, key=None):
        edges = [uv]

        a, b = uv
        end = b
        while True:
            if self.vertex_degree(a) != 4:
                break
            if a == end:
                break
            if key is not None and a == key:
                break
            if self.get_vertex_attribute(a, 'is_anchor'):
                break
            nbrs = self.vertex_neighbors(a, ordered=True)
            i = nbrs.index(b)
            b = nbrs[i - 2]
            edges.append((a, b))
            a, b = b, a

        b, a = uv
        end = b
        while True:
            if self.vertex_degree(a) != 4:
                break
            if a == end:
                break
            if key is not None and a == key:
                break
            if self.get_vertex_attribute(a, 'is_anchor'):
                break
            nbrs = self.vertex_neighbors(a, ordered=True)
            i = nbrs.index(b)
            b = nbrs[i - 2]
            edges.append((a, b))
            a, b = b, a

        edgeset = set(list(self.edges()))
        return [(u, v) if (u, v) in edgeset else (v, u) for u, v in edges]

    def get_parallel_edges(self, uv):
        edges = [uv]

        a, b = a0, b0 = uv
        while True:
            f = self.halfedge[a][b]
            if f is None:
                break
            vertices = self.face_vertices(f)
            if len(vertices) != 4:
                break
            i = vertices.index(a)
            a = vertices[i - 1]
            b = vertices[i - 2]
            if a in (a0, b0) and b in (a0, b0):
                break
            edges.append((a, b))

        edges[:] = edges[::-1]

        b, a = b0, a0 = uv
        while True:
            f = self.halfedge[a][b]
            if f is None:
                break
            vertices = self.face_vertices(f)
            if len(vertices) != 4:
                break
            i = vertices.index(a)
            a = vertices[i - 1]
            b = vertices[i - 2]
            if a in (a0, b0) and b in (a0, b0):
                break
            edges.append((a, b))

        edgeset = set(list(self.edges()))
        return [(u, v) if (u, v) in edgeset else (v, u) for u, v in edges]

    def draw(self, settings):
        from compas_fofin.rhino import ShellArtist

        artist = ShellArtist(self, layer=settings.get('layer'))
        artist.clear_layer()

        if settings.get('show.vertices'):
            color = {key: '#ff0000' for key in self.vertices_where({'is_anchor': True})}
            artist.draw_vertices(color=color)
        if settings.get('show.edges'):
            artist.draw_edges()
        if settings.get('show.faces'):
            if settings.get('join.faces'):
                artist.draw_mesh()
            else:
                artist.draw_faces()
        if settings.get('show.forces'):
            artist.draw_forces()
        if settings.get('show.reactions'):
            artist.draw_reactions()
        if settings.get('show.residuals'):
            artist.draw_residuals()

        artist.redraw()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
