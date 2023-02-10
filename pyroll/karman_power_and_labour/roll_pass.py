from pyroll.core import RollPass, Hook
from pyroll.karman_power_and_labour.karman_solver import KarmanSolver


@RollPass.extension_class
class RollPassExt(RollPass):
    coulomb_friction_coefficient = Hook[float]()
    """Friction coefficient according to Coulombs model."""
    karman_solution = Hook[KarmanSolver]()
    """Solution values of von-Karman ODE"""


@RollPassExt.coulomb_friction_coefficient
def coulomb_friction_coefficient(self: RollPassExt):
    raise ValueError(
        "You must provide Coulomb's friction coefficient to use the pyroll-karman-power-and-labour plugin.")


@RollPassExt.mean_front_tension
def mean_front_tension(self: RollPassExt):
    raise ValueError(
        "You must provide a mean front tension to use the pyroll-karman-power-and-labour plugin.")


@RollPassExt.mean_back_tension
def mean_back_tension(self: RollPassExt):
    raise ValueError(
        "You must provide a mean back tension to use the pyroll-karman-power-and-labour plugin.")


@RollPassExt.karman_solution
def karman_solution(self: RollPassExt):
    return KarmanSolver(roll_pass=self)


@RollPassExt.roll_force
def roll_force(self: RollPassExt):
    return (self.karman_solution.roll_force_per_unit_width * self.roll.contact_area) / self.roll.contact_length


@RollPassExt.mean_neutral_plane_position
def mean_neutral_plane_position(self: RollPassExt):
    return self.karman_solution.neutral_plane_position


@RollPassExt.Roll.roll_torque
def roll_torque(self: RollPassExt.Roll):
    return (
            self.roll_pass.karman_solution.roll_torque_per_unit_width * self.roll_pass.contact_area) / self.contact_length
