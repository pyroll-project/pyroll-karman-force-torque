import pyroll
from pyroll.core import RollPass, Hook

RollPass.DiskElement.equivalent_height_derivative = Hook[float]()
RollPass.DiskElement.direction = Hook[float]()
RollPass.DiskElement.longitudinal_stress_increment = Hook[float]()
RollPass.DiskElement.OutProfile.equivalent_longitudinal_angle = Hook[float]()

pyroll.core.root_hooks.add(pyroll.core.RollPass.coulomb_friction_coefficient)

pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.direction)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.longitudinal_stress_increment)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.equivalent_height_derivative)


pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.equivalent_longitudinal_angle)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.longitudinal_stress)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.altitudinal_stress)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.normal_stress)
pyroll.core.root_hooks.add(pyroll.core.RollPass.DiskElement.OutProfile.longitudinal_contact_friction)

