import numpy as np

from scipy.integrate import trapezoid

from pyroll.core import RollPass


@RollPass.roll_force
def roll_force(self: RollPass):
    def _gen_altitudinal_stress():
        yield self.disk_elements[0].in_profile.x, self.disk_elements[0].in_profile.altitudinal_stress
        for de in self.disk_elements:
            yield de.out_profile.x, de.out_profile.altitudinal_stress

    x, altitudinal_stress = np.array(list(_gen_altitudinal_stress())).T
    try:
        integral = trapezoid(altitudinal_stress, x)

    except AttributeError:  # first iteration: disks are not solved
        return self.in_profile.flow_stress * self.roll.contact_area * 2

    return (integral * self.contact_area) / self.roll.contact_length
