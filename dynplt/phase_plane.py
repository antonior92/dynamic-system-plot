"""
Phase plane plot function
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

__all__ = [
    'phase_plane'
]


def phase_plane(odeobject, initial_conditions, display_window,
                nvectors=[20, 20], calculation_window=None,
                solution_direction='both',
                markinitialpoint=False, ax=None):
    """
    Plot vector field and solution curves in the phase plane
    for planar autonomous systems.

    Parameters
    ----------
    odeobject : callable
        A generic interface class to numeric integrators, defined
        in scipy.integrate.
    initial_conditions : array of arrays
        A list containing a set of initial conditions. For each
        of these initial conditions the system will be simulated
        and plot in the phase plane
    display_window : array_like
        Contain 4 elements, respectively, the  lower limit and upper
        limits of x and y axis.
    nvectors : array_like, optional
        A list containing 2 elements, the number of columns and rows
        on the vector field grid. By default [20, 20].
    calculation_window : array_like, optional
        Contain 4 elements, respectively, the  lower limit and upper
        limits of x and y axis. By default, 4 times the display window
        in every direction.
    solution_direction : str, optional
        The solution can go 'foward', 'backward' or 'both'. The default
        is 'both'
    markinitialpoint : boolean, optional
        If True mark the initial point on the plot. By default it is False.
    ax : matplotlib axis object, optional
        Axis in which the phase plane will be plot. If none is provided
        create a new one.
    """

    # Create new subplot if no axis is provided
    if ax is None:
        _, ax = plt.subplots()

    # If no calculation window is provided, define one from display_window
    if calculation_window is None:
        x1mean = np.mean(display_window[:2])
        x2mean = np.mean(display_window[2:])
        x1min = display_window[0]
        x1max = display_window[1]
        x2min = display_window[2]
        x2max = display_window[3]
        calculation_window = [(x1min-x1mean)*4+x1mean,
                              (x1max-x1mean)*4+x1mean,
                              (x2min-x2mean)*4+x2mean,
                              (x2max-x2mean)*4+x2mean]

    # Define lower and upper limits from calculation_window
    lower_limit = [calculation_window[0], calculation_window[2]]
    upper_limit = [calculation_window[1], calculation_window[3]]

    # Get function from odeobject object
    def func(z):
        return odeobject.f(0, z, *odeobject.f_params)

    # Generate grid of points
    x = np.linspace(display_window[0], display_window[1], nvectors[0])
    y = np.linspace(display_window[2], display_window[3], nvectors[1])
    x, y = np.meshgrid(x, y)

    # Compute vector field
    xv = np.zeros_like(x)
    yv = np.zeros_like(y)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            state2d = np.array([x[i, j], y[i, j]])
            state2d_derivative = func(state2d)
            xv[i, j] = state2d_derivative[0]
            yv[i, j] = state2d_derivative[1]

    # Normalize vector field
    norm = np.hypot(xv, yv)
    norm[norm == 0] = 1
    xv, yv = xv/norm, yv/norm

    # Plot vector Field
    ax.quiver(x, y, xv, yv, norm, pivot='mid', units='xy', cmap=cm.plasma)


    # Set simulation parameters
    t1 = 100*1/np.mean(norm)*(np.max(upper_limit)-np.min(lower_limit))
    dt = 1/100*1/np.mean(norm)*(np.max(upper_limit)-np.min(lower_limit))

    for x0 in initial_conditions:
        foward = []
        backward = []
        if solution_direction is'foward' or solution_direction is'both':
            odeobject.set_initial_value(x0)
            while odeobject.successful() and odeobject.t < t1:
                xnext = odeobject.integrate(odeobject.t+dt)
                if np.logical_or(xnext < lower_limit,
                                 xnext > upper_limit).any():
                    break
                foward.append(xnext)

        if solution_direction is 'backward' or solution_direction is'both':
            odeobject.set_initial_value(x0)
            while odeobject.successful() and odeobject.t > -1*t1:
                xnext = odeobject.integrate(odeobject.t-dt)
                if np.logical_or(xnext < lower_limit,
                                 xnext > upper_limit).any():
                    break
                backward.append(xnext)

        if markinitialpoint:
            ax.plot(x0[0], x0[1], marker='o', markersize=5, color='black')

        x0 = np.reshape(x0, (-1, 2))
        foward = np.reshape(foward, (-1, 2))
        backward = np.reshape(backward[::-1], (-1, 2))

        x = np.concatenate((backward, x0, foward), axis=0)

        ax.plot(x[:, 0], x[:, 1], linewidth=1.5)

    ax.axis(display_window)

    return
