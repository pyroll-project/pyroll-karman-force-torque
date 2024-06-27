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

        def _gen_altitudinal_stress():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].in_profile.altitudinal_stress
            for de in unit.disk_elements:
                yield de.out_profile.x, de.out_profile.altitudinal_stress

        def _gen_shear_stress():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].in_profile.longitudinal_contact_friction
            for de in unit.disk_elements:
                yield de.out_profile.x, de.out_profile.longitudinal_contact_friction

        def _gen_longitudinal_stress():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].in_profile.longitudinal_stress
            for de in unit.disk_elements:
                yield de.out_profile.x, de.out_profile.longitudinal_stress

        def _gen_normal_stress():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].in_profile.normal_stress
            for de in unit.disk_elements:
                yield de.out_profile.x, de.out_profile.normal_stress

        def _gen_flow_stress():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].in_profile.flow_stress
            for de in unit.disk_elements:
                yield de.out_profile.x, de.out_profile.flow_stress

        x, flow_stress = np.array(list(_gen_flow_stress())).T
        x, altitudinal_stress = np.array(list(_gen_altitudinal_stress())).T
        x, shear_stress = np.array(list(_gen_shear_stress())).T
        x, longitudinal_stress = np.array(list(_gen_longitudinal_stress())).T
        x, normal_stress = np.array(list(_gen_normal_stress())).T

        ax.plot(x * 1e3, altitudinal_stress * 1e-6, label=r"$\sigma_y$")
        ax.plot(x * 1e3, shear_stress * 1e-6, label=r"$\tau_r$")
        ax.plot(x * 1e3, longitudinal_stress * 1e-6, label=r"$\sigma_x$")
        ax.plot(x * 1e3, normal_stress * 1e-6, label=r"$\sigma_n$")
        ax.plot(x * 1e3, flow_stress * 1e-6, label=r"k_f")

        ax.legend()
        return fig


@hookimpl(specname="unit_plot")
def roll_pass_disk_element_direction_plot(unit: RollPass):
    if isinstance(unit, RollPass) and unit.disk_elements:
        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.subplots()
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel(" - ")
        ax.set_title("RollPass Disk Element Direction")

        def _gen():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].direction
            for de in unit.disk_elements:
                yield de.out_profile.x, de.direction

        x, direction = np.array(list(_gen())).T
        ax.plot(x, direction, label="DiskElement Direction")

        ax.axvline(unit.roll.neutral_point, label="neutral plane", ls="--", c="green")

        ax.legend()
        return fig


@hookimpl(specname="unit_plot")
def roll_pass_geometry(unit: RollPass):
    if isinstance(unit, RollPass) and unit.disk_elements:
        fig: plt.Figure = plt.figure()
        ax: plt.Axes = fig.subplots()
        ax.grid(True)
        ax.set_xlabel("x")
        ax.set_ylabel(" - ")
        ax.set_title("RollPass Geometry")

        def _gen_eq_height():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].in_profile.equivalent_height
            for de in unit.disk_elements:
                yield de.out_profile.x, de.out_profile.equivalent_height

        def _gen_eq_angle():
            yield unit.disk_elements[0].in_profile.x, unit.disk_elements[0].in_profile.equivalent_longitudinal_angle
            for de in unit.disk_elements:
                yield de.out_profile.x, de.out_profile.equivalent_longitudinal_angle

        x, equivalent_height = np.array(list(_gen_eq_height())).T
        x, equivalent_longitudinal_angle = np.array(list(_gen_eq_angle())).T

        ax.plot(x, equivalent_height, label="Equivalent Height")
        ax.plot(x, equivalent_longitudinal_angle, label="Equivalent Longitudinal Angle")

        ax.legend()
        return fig
