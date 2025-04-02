import os
import subprocess as sp
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set()

prog_directory = r"Z:\other"
executable = "graph.exe"
full_executable_path = os.path.join(prog_directory, executable)

probs = [x / 10 for x in range(1, 11, 1)]
n_vertices = [x for x in range(5, 50, 10)]
n_trials = 1000


def single_experiment(n_vert: int, prob: float):
    if not os.path.exists(full_executable_path):
        raise FileNotFoundError(f"Executable not found at {full_executable_path}")

    process = sp.Popen(
        [full_executable_path, str(n_vert), str(prob)],
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        cwd=prog_directory,
        text=True
    )

    stdout, stderr = process.communicate()
    # if stderr:
    #     print(f"Error: \n{stderr.rstrip()}")
    # print(f"Output: \n{stdout.rstrip()}")

    n_components, n_edges, n_cycles = stdout.rstrip().split()

    return n_components, n_edges, n_cycles


def multiple_experiments():
    fig, ax = plt.subplots()
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    for vert in n_vertices:
        n_comp_means = []
        n_comp_std = []

        n_edges_means = []
        n_edges_std = []

        n_cycles_means = []
        n_cycles_std = []

        for prob in probs:
            n_components_data = []
            n_edges_data = []
            n_cycles_data = []

            for i in range(n_trials):
                n_comp, n_edges, n_cycles = single_experiment(vert, prob)

                n_components_data.append(int(n_comp))
                n_edges_data.append(int(n_edges))
                n_cycles_data.append(int(n_cycles))

            n_comp_std.append(np.std(n_components_data))
            n_comp_means.append(np.mean(n_components_data))

            n_edges_std.append(np.std(n_edges_data))
            n_edges_means.append(np.mean(n_edges_data))

            n_cycles_std.append(np.std(n_cycles_data))
            n_cycles_means.append(np.mean(n_cycles_data))

        ax.plot(probs, n_comp_means, label=f"vertice = {vert}")
        ax.fill_between(probs, np.array(n_comp_means) - np.array(n_comp_std),
                        np.array(n_comp_means) + np.array(n_comp_std), alpha=0.15)
        ax.legend()

        ax1.plot(probs, n_edges_means, label=f"vertice = {vert}")
        ax1.fill_between(probs, np.array(n_edges_means) - np.array(n_edges_std),
                         np.array(n_edges_means) + np.array(n_edges_std), alpha=0.15)
        ax1.legend()

        ax2.plot(probs, n_cycles_means, label=f"vertice = {vert}")
        ax2.fill_between(probs, np.array(n_cycles_means) - np.array(n_cycles_std),
                         np.array(n_cycles_means) + np.array(n_cycles_std), alpha=0.15)
        ax2.legend()

    plt.show()


def main():
    multiple_experiments()


if __name__ == "__main__":
    main()
