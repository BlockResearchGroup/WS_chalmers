from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

try:
    from numpy import array
    from numpy import float64
    from scipy.sparse import diags
    from scipy.sparse.linalg import spsolve

except ImportError:
    compas.raise_if_not_ironpython()

from compas.numerical import normrow
from compas.numerical import connectivity_matrix

from compas_fofin.utilities import NumericalSelfweightCalculator


__all__ = [
    'shell_update_xyz_numpy',
    'shell_update_xyz_numpy_proxy'
]


def shell_update_xyz_numpy_proxy(data):
    """Proxy for remote procedure call to ``compas_fofin.datastructures.shell_update_xyz_numpy``.

    Parameters
    ----------
    data : dict
        The data representing the shell data structure.

    Returns
    -------
    dict
        The data dict of the updated shell.

    """
    from compas_fofin.datastructures import Shell
    shell = Shell.from_data(data)
    shell_update_xyz_numpy(shell)
    return shell.to_data()


def shell_update_xyz_numpy(shell):
    """Compute the equilibrium shape of the shell using the force density method.

    Parameters
    ----------
    shell : compas_fofin.datastructures.Shell
        The shell data structure.

    """
    k_i   = shell.key_index()
    fixed = shell.vertices_where({'is_anchor': True})
    fixed = [k_i[key] for key in fixed]
    free  = list(set(range(shell.number_of_vertices())) - set(fixed))
    xyz   = array(shell.get_vertices_attributes('xyz'), dtype=float64)
    p     = array(shell.get_vertices_attributes(('px', 'py', 'pz')), dtype=float64)
    edges = [(k_i[u], k_i[v]) for u, v in shell.edges_where({'is_edge': True})]
    q     = array([attr['q'] for u, v, attr in shell.edges_where({'is_edge': True}, True)], dtype=float64).reshape((-1, 1))
    C     = connectivity_matrix(edges, 'csr')
    Ct    = C.transpose()
    Ci    = C[:, free]
    Cf    = C[:, fixed]
    Cit   = Ci.transpose()

    calculate_sw = NumericalSelfweightCalculator(shell, density=shell.attributes['density'], thickness_attr_name='c1')
    sw = calculate_sw(xyz)
    p[:, 2] = - sw[:, 0]

    Q = diags([q.flatten()], [0])
    A = Cit.dot(Q).dot(Ci)
    b = p[free] - Cit.dot(Q).dot(Cf).dot(xyz[fixed])

    xyz[free] = spsolve(A, b)

    l = normrow(C.dot(xyz))
    f = q * l
    r = p - Ct.dot(Q).dot(C).dot(xyz)

    for index, (key, attr) in enumerate(shell.vertices(True)):
        attr['x']  = xyz[index, 0]
        attr['y']  = xyz[index, 1]
        attr['z']  = xyz[index, 2]
        attr['rx'] = r[index, 0]
        attr['ry'] = r[index, 1]
        attr['rz'] = r[index, 2]

    for index, (u, v, attr) in enumerate(shell.edges_where({'is_edge': True}, True)):
        attr['q'] = q[index, 0]
        attr['f'] = f[index, 0]
        attr['l'] = l[index, 0]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
