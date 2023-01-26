import numpy as np
from pyroll.core import RollPass
from pyroll.freiberg_flow_stress import freiberg_flow_stress


class AlexanderSolver:
    """Class representing the Alexander solution algorithm for the slab theory of von Karman."""

    def __int__(self, roll_pass: RollPass):
        self.roll_pass = roll_pass
        self.slab_element_count = 100
        self.step_width = self.roll_pass.roll.contact_length / self.slab_element_count
        self.angular_coordinates = self.discretize_roll_gap_in_angular_coordinates()
        self.local_heights = self.local_mean_height()
        self.initial_mean_neutral_plane = np.tan(1 / 2 *
            np.sqrt(self.roll_pass.out_profile.equivalent_height / self.roll_pass.roll.working_radius) *
            np.arctan(self.roll_pass.roll.working_radius / self.roll_pass.out_profile.equivalent_height) *
                                                 self.angular_coordinates[0] - 1 /2 * self.roll_pass.out_profile.equivalent_height / self.roll_pass.roll.working_radius * self.roll_pass.log_draught)

    def discretize_roll_gap_in_angular_coordinates(self):
        horizontal_coordinates = np.arange(start=-self.roll_pass.roll.contact_length, stop=0,
                                           step=self.step_width)

        angular_coordinates = [-np.arcsin(horizontal_coordinate / self.roll_pass.roll.working_radius) for
                               horizontal_coordinate in horizontal_coordinates]
        return angular_coordinates

    def local_mean_height(self):
        return [self.roll_pass.out_profile.equivalent_height + 2 * self.roll_pass.roll.working_radius(
            1 - np.cos(angular_coordinate)) for
                angular_coordinate in self.angular_coordinates]

    def equivalent_forming_values(self):
        pass

    def flow_stress_along_roll_gap(self):
        strains = [np.log(
            (local_height - self.roll_pass.in_profile.equivalent_height) / self.roll_pass.in_profile.equivalent_height)
            for local_height in self.local_heights]
        strain_rates =
        return [freiberg_flow_stress(strain=_strain) for _strain in strains]

    def normal_pressure_at_plastic_entry(self):
        pass

    def normal_pressure(self):
        pass
