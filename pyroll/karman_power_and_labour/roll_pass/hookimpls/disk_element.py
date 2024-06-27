import numpy as np
from pyroll.core import RollPass


@RollPass.DiskElement.equivalent_height_derivative
def equivalent_height_derivative(self: RollPass.DiskElement):
    return (self.out_profile.equivalent_height - self.in_profile.equivalent_height) / self.length


@RollPass.DiskElement.OutProfile.equivalent_longitudinal_angle
def equivalent_longitudinal_angle(self: RollPass.DiskElement):
    return - np.arcsin(self.x / self.roll_pass.roll.working_radius)

@RollPass.DiskElement.direction
def direction(self: RollPass.DiskElement):
    from ... import Config
    return 2 / np.pi * np.arctan(
        (self.roll_pass.velocity - self.out_profile.velocity) / Config.SHEAR_STRESS_DIRECTION_REGULARISATION)


@RollPass.DiskElement.longitudinal_stress_increment
def longitudinal_stress_increment(self: RollPass.DiskElement):
    ip = self.in_profile
    return - (ip.longitudinal_stress * self.equivalent_height_derivative + 2 * ip.longitudinal_contact_friction - 2 * ip.normal_stress * np.tan(ip.equivalent_longitudinal_angle)) / ip.equivalent_height


@RollPass.DiskElement.OutProfile.longitudinal_stress
def longitudinal_stress(self: RollPass.DiskElement.OutProfile):
    return self.disk_element.in_profile.longitudinal_stress + self.disk_element.longitudinal_stress_increment * self.disk_element.length


@RollPass.DiskElement.OutProfile.normal_stress
def normal_stress(self: RollPass.DiskElement.OutProfile):
    return - self.altitudinal_stress - self.longitudinal_contact_friction * np.tan(self.equivalent_longitudinal_angle)


@RollPass.DiskElement.OutProfile.altitudinal_stress
def altitudinal_stress(self: RollPass.DiskElement.OutProfile):
    return self.longitudinal_stress - 2 / np.sqrt(3) * self.flow_stress


@RollPass.DiskElement.OutProfile.longitudinal_contact_friction
def longitudinal_contact_friction(self: RollPass.DiskElement.OutProfile):
    from ... import Config
    coulombs_normal_pressure = - self.altitudinal_stress / (1 + self.roll_pass.coulomb_friction_coefficient * np.tan(self.equivalent_longitudinal_angle) * self.direction)

    critical_normal_pressure = self.roll_pass.friction_factor * self.flow_stress / (np.sqrt(3) * self.roll_pass.coulomb_friction_coefficient)

    shear_stress_transition = np.arctan((coulombs_normal_pressure - critical_normal_pressure) / Config.SHEAR_STRESS_PRESSURE_REGULARISATION) / np.pi + 1/2

    return (self.roll_pass.coulomb_friction_coefficient * coulombs_normal_pressure * (1 - shear_stress_transition) + self.roll_pass.friction_factor * self.flow_stress / np.sqrt(3) * shear_stress_transition) * self.disk_element.direction



