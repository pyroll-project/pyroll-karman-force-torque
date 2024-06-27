import numpy as np
from pyroll.core import RollPass


def corner_correction_for_strain(self: RollPass):
    return np.tan(self.entry_angle) ** 2 / (2 * np.sqrt(3))


def corner_correction_for_longitudinal_stress(self: RollPass):
    return self.in_profile.flow_stress / 4 * (2 * np.tan(self.entry_angle) ** 2) / (2 * np.tan(self.entry_angle))


def initial_values(self: RollPass):
    ip = self.in_profile

    ip.strain = corner_correction_for_strain(self)
    ip.longitudinal_stress = corner_correction_for_longitudinal_stress(self) + self.back_tension

    ip.direction = 1
    ip.equivalent_longitudinal_angle = self.entry_angle

    ip.altitudinal_stress = ip.longitudinal_stress - 2 / np.sqrt(3) * self.in_profile.flow_stress
    ip.longitudinal_contact_friction = self.friction_factor * ip.flow_stress / np.sqrt(3)
    ip.normal_stress = - ip.altitudinal_stress - ip.longitudinal_contact_friction * np.tan(self.entry_angle)


RollPass.additional_inits.append(initial_values)
