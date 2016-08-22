from dynplt import cobweb
import matplotlib.pyplot as plt

def func(x, mu):
    return mu*x*(1-x)

mu = 3.6

_, ax = plt.subplots()
cobweb(func, 0.05, 10, [0, 1], args=(mu,), ax=ax)
ax.set_xlabel("x", fontsize=16)
ax.set_ylabel("y", fontsize=16)
ax.set_title("Cobweb Plot: Logistic Map", fontsize=18)
plt.show()
