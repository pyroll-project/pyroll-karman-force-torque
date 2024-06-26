import numpy as np
from pyroll.core import RollPass


def initial_values(self: RollPass):
    ip = self.in_profile

    ip.direction = 1
    ip.longitudinal_stress = self.back_tension
    ip.altitudinal_stress = ip.longitudinal_stress - 2 / np.sqrt(3) * self.in_profile.flow_stress


RollPass.additional_inits.append(initial_values)
