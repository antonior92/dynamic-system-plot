from dynplt import phase_plane
import numpy as np
import matplotlib.pyplot as plt


# Van der Poll oscilator
def vanderpoll(x, mu):
    dx = np.zeros(2)
    dx[0] = x[1]
    dx[1] = mu*(1-x[0]**2)*x[1]-x[0]

    return dx

# Define initial conditions and simulation times
initial_conditions = [[0.1, 0.1],
                      [-0.1, 0.1],
                      [-0.1, -0.1],
                      [0.1, -0.1],
                      [0.2, 0.2],
                      [-0.2, 0.2],
                      [-0.2, -0.2],
                      [0.2, -0.2],
                      [0.4, 0.4],
                      [-0.4, 0.4],
                      [-0.4, -0.4],
                      [0.4, -0.4],
                      [2, -4],
                      [-2, 4],
                      [1, -4],
                      [-1, 4],
                      [2, -3],
                      [-2, 3],
                      [1, -3],
                      [-1, 3]]
simulation_times = [np.linspace(0, 100, 10000)]*len(initial_conditions)
mu = 2

# Create axis
_, ax = plt.subplots()

# plot_phase_plane function
phase_plane(vanderpoll, initial_conditions, simulation_times,
            [-6, 6, -6, 6], args=(mu,), ax=ax)

ax.set_xlabel("x", fontsize=16)
ax.set_ylabel("y", fontsize=16)
ax.set_title("Phase Plane: van der Poll Equation", fontsize=18)
plt.show()
