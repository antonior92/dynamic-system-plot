"""
Cobweb plot function
"""

import numpy as np
import matplotlib.pyplot as plt

__all__ = [
    'cobweb'
]


def cobweb(func, initial_conditon, nsteps, limits, args=(), ax=None):
    """
    Plot cobweb diagram for onedimensional iterated functions
    ``x[n+1] = func(x[n])``.

    Parameters
    ----------
    func : callable
        Function that compute the next system state from the current one.
    initial_conditon : float
        Simulation initial condition.
    nsteps : int
        Number of steps displayed be the cobweb diagram.
    limits : 2 elements array_like
        Upper and lower limits for the cobweb diagram.
    arg : tuple, optional
        Extra arguments to pass to function ``func``.
    ax : matplotlib axis object, optional
        Axis in which the phase plane will be plot. If none is provided
        create a new one.
    """

    # Create new subplot if no axis is provided
    if ax is None:
        _, ax = plt.subplots()

    # Plot basic curves
    x = np.linspace(limits[0], limits[1], 1000)
    y = list(map(lambda z: func(z, *args), x))

    plt.plot(x, x, linewidth=1.5, color='black')
    plt.plot(x, y, linewidth=1.5, color='blue')

    # Interate and plot cobweb segments
    startpoint = initial_conditon
    for i in range(nsteps):
        endpoint = func(startpoint, *args)
        plt.plot([startpoint, startpoint, endpoint],
                 [startpoint, endpoint, endpoint],
                 color='red',
                 marker='o',
                 markersize=3,
                 markerfacecolor='black')
        startpoint = endpoint
