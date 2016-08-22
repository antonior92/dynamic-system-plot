"""
Phase plane plot function
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import scipy.integrate

__all__ = [
    'phase_plane'
]


def phase_plane(func,  initial_conditions,
                simulation_times, limits,
                args=(), odeint=scipy.integrate.odeint,
                nvectors=[20, 20], ax=None):
    """
    Plot vector field and solution curves in the phase plane
    for planar autonomous systems.

    Parameters
    ----------
    func : callable
        Function that relates the point and the derivative for a
        planar autonomous systems ``dx/dt = func(x)``.
    initial_conditions : array of arrays
        A list containing a set of initial conditions. For each
        of these initial conditions the system will be simulated
        and plot in the phase plane
    simulation_time : array of arrays
        A list containing simulation times. One for each one of
        of the initial conditions. Each simulation time is a
        sequence of time points for which to solve for y. The
        initial value point should be the first element of
        this sequence.
    limits : 4 elements array_like
        A list containing 4 elements, respectively: lower limit
        for x axis, upper limit for x axis, lower limit for y axis
        and upper limit for x axis.
    args : tuple, optional
        Extra arguments to pass to function ``func``.
    odeint : callable, optional
        Solver for ordinary differential equations. Solvers should
        have the signature ``odeint(auxfunc, x0, t,)`` and should
        work with non-autonomous systems ``auxfunc(x, t)``. By
        default uses ``scipy.integrate.odeint``.
    nvectors : 2 elements array_like, optional
        A list containing 2 elements, the number of columns and rows
        on the vector field grid. By default [20, 20].
    ax : matplotlib axis object, optional
        Axis in which the phase plane will be plot. If none is provided
        create a new one.
    """

    # Create new subplot if no axis is provided
    if ax is None:
        _, ax = plt.subplots()

    # check initial_conditions and simulation_time
    if len(simulation_times) != len(initial_conditions):
        raise ValueError("Simulation time and initial_conditions should \
        have the same dimensions along the axis 0.")

    # define auxiliar function
    def auxfunc(x, t):
        return func(x, *args)

    # simulate and plot the solutions for each one of the initial conditions
    for i in range(len(simulation_times)):
        state = odeint(auxfunc, initial_conditions[i], simulation_times[i])
        ax.plot(state[:, 0], state[:, 1], linewidth=1.5)
        ax.plot(initial_conditions[i][0], initial_conditions[i][1],
                marker='o', markersize=5, color='black')

    # Generate grid of points
    x = np.linspace(limits[0], limits[1], nvectors[0])
    y = np.linspace(limits[2], limits[3], nvectors[1])
    x, y = np.meshgrid(x, y)

    # Compute vector field
    xv = np.zeros_like(x)
    yv = np.zeros_like(y)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            state2d = np.array([x[i, j], y[i, j]])
            state2d_derivative = func(state2d, *args)
            xv[i, j] = state2d_derivative[0]
            yv[i, j] = state2d_derivative[1]

    # Normalize vector field
    norm = np.hypot(xv, yv)
    norm[norm == 0] = 1
    xv, yv = xv/norm, yv/norm

    # Plot vector Field
    ax.quiver(x, y, xv, yv, norm, pivot='mid', units='xy', cmap=cm.plasma)
    ax.axis(limits)

    return
