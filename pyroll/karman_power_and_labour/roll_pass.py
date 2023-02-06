from pyroll.core import RollPass, Hook
from pyroll.karman_power_and_labour.karman_solver import KarmanSolver


@RollPass.extension_class
class RollPass(RollPass):
    coulomb_friction_coefficient = Hook[float]()
    """Friction coefficient according to Coulombs model."""
    karman_solution = Hook[KarmanSolver]()
    """Solution values of von-Karman ODE"""


@RollPass.coulomb_friction_coefficient
def coulomb_friction_coefficient(self: RollPass):
    raise ValueError(
        "You must provide Coulomb's friction coefficient to use the pyroll-karman-power-and-labour plugin.")


@RollPass.mean_front_tension
def mean_front_tension(self: RollPass):
    raise ValueError(
        "You must provide a mean front tension to use the pyroll-karman-power-and-labour plugin.")


@RollPass.mean_back_tension
def mean_back_tension(self: RollPass):
    raise ValueError(
        "You must provide a mean back tension to use the pyroll-karman-power-and-labour plugin.")


@RollPass.karman_solution
def karman_solution(self: RollPass):
    return KarmanSolver(roll_pass=self)


@RollPass.roll_force
def roll_force(self: RollPass):
    return (self.karman_solution.roll_force_per_unit_width * self.roll.contact_area) / self.roll.contact_length


@RollPass.Roll.roll_torque
def roll_torque(self: RollPass.Roll):
    return (self.roll_pass.karman_solution.roll_torque_per_unit_width * self.roll_pass.contact_area) / self.contact_length