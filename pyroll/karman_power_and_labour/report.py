import numpy as np
import matplotlib.pyplot as plt

from pyroll.core import Unit, RollPass
from pyroll.report import hookimpl


@hookimpl(specname="unit_plot")
def roll_pass_stress_profile_plot(unit: RollPass):
    if isinstance(unit, RollPass) and unit.disk_elements:
        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.subplots()
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel(" - ")
        ax.set_title("RollPass Stress Profile")

        def _gen():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].in_profile.altitudinal_stress
            for de in unit.disk_elements:
                yield de.out_profile.x, de.out_profile.altitudinal_stress

        x, altitudinal_stress = np.array(list(_gen())).T
        ax.plot(x, altitudinal_stress, label="Altitudinal Stress")

        ax.axvline(unit.roll.neutral_point, label="neutral plane", ls="--", c="green")

        ax.legend()
        return fig


@hookimpl(specname="unit_plot")
def roll_pass_flow_stress_plot(unit: RollPass):
    if isinstance(unit, RollPass) and unit.disk_elements:
        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.subplots()
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel(" - ")
        ax.set_title("RollPass Stress Profile")

        def _gen():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].in_profile.flow_stress
            for de in unit.disk_elements:
                yield de.out_profile.x, de.out_profile.flow_stress

        x, flow_stress = np.array(list(_gen())).T
        ax.plot(x, flow_stress, label="Flow Stress")

        ax.axvline(unit.roll.neutral_point, label="neutral plane", ls="--", c="green")

        ax.legend()
        return fig