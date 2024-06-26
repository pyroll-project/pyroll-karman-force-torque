import numpy as np

from pyroll.core import RollPass


@RollPass.InProfile.normal_stress
def normal_stress(self: RollPass.DiskElement.OutProfile):
    return -self.altitudinal_stress - self.longitudinal_contact_friction + np.tan(self.longitudinal_angle)


@RollPass.InProfile.longitudinal_contact_friction
def longitudinal_contact_friction(self: RollPass.InProfile):
    from ... import Config
    coulombs_normal_pressure = - self.normal_stress / (1 + self.roll_pass.coulomb_friction_coefficient * np.tan(
        self.longitudinal_angle) * self.direction)
    critical_normal_pressure = self.roll_pass.friction_factor * self.flow_stress / (
            np.sqrt(3) * self.roll_pass.coulomb_friction_coefficient)
    shear_stress_transition = 1 / np.pi * np.arctan(
        (coulombs_normal_pressure - critical_normal_pressure) / Config.SHEAR_STRESS_PRESSURE_REGULARISATION) + 0.5

    return self.roll_pass.coulomb_friction_coefficient * coulombs_normal_pressure * (
            1 - shear_stress_transition) + self.roll_pass.friction_factor * self.flow_stress / np.sqrt(
        3) * shear_stress_transition
