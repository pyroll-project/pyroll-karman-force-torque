import logging
import numpy as np
import pandas as pd
import scipy.interpolate as inter
import scipy.optimize as opt
from scipy.integrate import quad
from scipy.misc import derivative

from pyroll.core import RollPass


class KarmanSolver:
    """Class representing the solution of the von-Karman equation for a equivalent flat roll pass."""

    def __init__(self, roll_pass: RollPass):
        self.roll_pass = roll_pass
        self.slab_element_count = 100
        self.step_width = self.roll_pass.roll.contact_length / self.slab_element_count
        self.roll_gap_coordinates = np.arange(-self.roll_pass.roll.contact_length, 0, self.step_width)
        self.forward_solution = self.solve(solution_direction="forward")
        self.backward_solution = self.solve(solution_direction="backward")

        self.horizontal_stress_forward_interpolation = inter.interp1d(
            self.forward_solution.index, self.forward_solution["horizontal_stress"], fill_value="extrapolate")
        self.horizontal_stress_backward_interpolation = inter.interp1d(
            self.backward_solution.index, self.backward_solution["horizontal_stress"], fill_value="extrapolate")

        self.neutral_plane_position = opt.brentq(lambda position:
                                                 self.horizontal_stress_backward_interpolation(position)
                                                 - self.horizontal_stress_forward_interpolation(position),
                                                 - self.roll_pass.roll.contact_length, 0)
        self.solution = pd.concat(
            [self.forward_solution[-self.roll_pass.roll.contact_length: self.neutral_plane_position],
             self.backward_solution[0: self.neutral_plane_position]]).sort_index()
        self.vertical_stress = inter.interp1d(self.solution.index, self.solution["vertical_stress"],
                                              fill_value="extrapolate")
        self.shear_stress = inter.interp1d(self.solution.index, self.solution["shear_stress"],
                                           fill_value="extrapolate")
        self.roll_force_per_unit_width = self.return_roll_force_per_unit_width()
        self.roll_torque_per_unit_width = self.return_roll_torque_per_unit_width()

    def equivalent_roll_gap_height(self, roll_gap_coordinate):
        return self.roll_pass.gap + 2 * (self.roll_pass.roll.working_radius - np.sqrt(
            self.roll_pass.roll.working_radius ** 2 - roll_gap_coordinate ** 2))

    def equivalent_local_strain(self, roll_gap_coordinate):
        return 2 / np.sqrt(3) * np.log(self.roll_pass.in_profile.equivalent_height / self.equivalent_roll_gap_height(
            roll_gap_coordinate))

    def solve(self, solution_direction: str):
        log = logging.getLogger(__name__)
        if solution_direction == "forward":
            start_position = -self.roll_pass.roll.contact_length
            exit_position = 0
            horizontal_stress = self.roll_pass.mean_back_tension
            direction = 1
        else:
            start_position = 0
            exit_position = -self.roll_pass.roll.contact_length
            horizontal_stress = self.roll_pass.mean_front_tension
            direction = -1

        position = start_position
        step_width_with_direction = self.step_width * direction
        solution_storage = {}

        while position < exit_position if direction > 0 else position > exit_position:
            height_derivate = derivative(self.equivalent_roll_gap_height, position, dx=1e-8)
            roll_angle = -np.arcsin(position / self.roll_pass.roll.working_radius)
            equivalent_strain = self.equivalent_local_strain(position)
            flow_stress = self.roll_pass.in_profile.flow_stress_function(strain=equivalent_strain,
                                                                         strain_rate=self.roll_pass.strain_rate,
                                                                         temperature=self.roll_pass.in_profile.temperature)
            vertical_stress = horizontal_stress - 2 / np.sqrt(3) * flow_stress
            normal_pressure = - vertical_stress / (
                    1 + self.roll_pass.coulomb_friction_coefficient * np.tan(roll_angle) * direction)
            shear_stress = self.roll_pass.coulomb_friction_coefficient * normal_pressure * direction

            solution_storage[position] = (
                {"horizontal_stress": horizontal_stress, "vertical_stress": vertical_stress,
                 "shear_stress": shear_stress,
                 "normal_pressure": normal_pressure, "flow_stress": flow_stress})

            horizontal_stress_change = - (
                    horizontal_stress * height_derivate + 2 * shear_stress - 2 * normal_pressure * np.tan(
                roll_angle)) / self.equivalent_roll_gap_height(
                position)
            horizontal_stress += horizontal_stress_change * step_width_with_direction
            position += step_width_with_direction

        log.debug(f"Finished solution of von-Karman ODE.")
        return pd.DataFrame.from_dict(solution_storage, orient="index")

    def return_roll_force_per_unit_width(self):
        integral = -quad(lambda position: self.vertical_stress(position), -self.roll_pass.roll.contact_length, 0)[0]
        return integral

    def return_roll_torque_per_unit_width(self):
        integral = quad(lambda position: self.shear_stress(position), -self.roll_pass.roll.contact_length, 0)[0]
        return integral
