#!/usr/bin/env python3
from sys import get_coroutine_origin_tracking_depth
import numpy as np
import matplotlib.pyplot as plt

my_rcParams = {
    "text.usetex": True,
    "font.family": "Georgia",
    "font.size": 32,
    "lines.linewidth": 3,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.major.size": 12,
    "ytick.major.size": 12,
    "xtick.minor.size": 6,
    "ytick.minor.size": 6,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "legend.frameon": False,
}
plt.rcParams.update(my_rcParams)


class HydroProfile:
    def __init__(
        self, i_eta_max: int, i_tau_max: int, i_x_max: int, n_info: int, fname: str
    ):
        self.n_eta = i_eta_max
        self.n_tau = i_tau_max
        self.n_x = i_x_max  ## same as n_y
        self.n_comp = n_info
        self._fname = fname
        self._hydro = None

    def read_file(self):
        self._hydro = np.fromfile(
            self._fname,
            dtype=np.float32,
            count=self.n_tau * self.n_eta * self.n_x * self.n_x * self.n_comp,
            sep="",
        )
        self._hydro = self._hydro.reshape(
            (self.n_tau, self.n_eta, self.n_x, self.n_x, self.n_comp)
        )

    def get_temperature_evolution_profile(self, eta: float = 0.0):
        eta_index = int((eta + 10) * (self.n_eta / 20.0))
        return self._hydro[:, eta_index, :, :, 0]


def compute_average(data, temperature_cut: float = 0.16):
    ## compute the average of the temperature above the
    ## provided cutoff
    temperature_evol_history = []
    for time in range(len(data)):
        tmp = [v for v in data[time].flatten() if v >= temperature_cut]
        if len(tmp) == 0:
            temperature_evol_history.append(0)
        else:
            temperature_evol_history.append(sum(tmp) / len(tmp))

    return temperature_evol_history


def get_extreme_temperature(data, maximum: bool = True, cutoff: float = 0.16):
    ## compute the average of the temperature above the
    ## provided cutoff
    temperature_evol_history = []
    f = max if maximum else min
    for time in range(len(data)):
        tmp = f(data[time].flatten())
        temperature_evol_history.append(tmp if maximum else max(tmp, cutoff))
    return temperature_evol_history


def main():
    hydro = HydroProfile(
        i_eta_max=64, i_tau_max=84, i_x_max=100, n_info=5, fname="evolution_xyeta.dat"
    )
    hydro.read_file()
    data = hydro.get_temperature_evolution_profile(eta=0)
    hist = compute_average(data, 0.16)
    maximum = get_extreme_temperature(data, maximum=True)
    times = 0.4 + np.arange(0, len(data)) * 0.2
    fig, ax = plt.subplots(
        1,
        1,
        figsize=(16, 9),
        gridspec_kw={"left": 0.08, "right": 0.99, "top": 0.99, "bottom": 0.1},
    )
    ax.plot(times, hist, color="blue", label="average", linestyle="solid")
    ax.plot(times, maximum, color="red", label="maximum", linestyle="dashed")
    ax.legend(loc="best")
    ax.set_ylabel("Temperature (MeV)")
    ax.set_xlabel(r"$\tau$ (fm$/c$)")
    plt.show()


if __name__ == "__main__":
    main()
