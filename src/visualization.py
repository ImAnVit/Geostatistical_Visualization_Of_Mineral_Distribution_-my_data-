import matplotlib.pyplot as plt

def plot_points(data, element="Ni"):
    plt.scatter(data["x"], data["y"], c=data[element], edgecolor='k')
    plt.colorbar(label=f"{element} concentration")
    plt.title(f"{element} Distribution (Sample Points)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()