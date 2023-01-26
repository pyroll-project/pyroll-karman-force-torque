import numpy as np
from pyroll.core import RollPass


class AlexanderSolver:
    """Class representing the Alexander solution algorithm for the slab theory of von Karman."""

    def __int__(self, roll_pass: RollPass):
        self.roll_pass = roll_pass
        self.slab_element_count = 100
        self.compressed_length = self.compressed_length()
        self.angular_coordinates = self.discretize_roll_gap_in_angular_coordinates()

    def compressed_length(self):
        ld = np.sqrt(self.roll_pass.roll.working_radius * (
                self.roll_pass.in_profile.equivalent_height - self.roll_pass.out_profile.equivalent_height) -
                     (self.roll_pass.in_profile.equivalent_height - self.roll_pass.out_profile.equivalent_height) ** (
                             2 / 4))
        return ld

    def discretize_roll_gap_in_angular_coordinates(self):
        horizontal_coordinates = np.arange(start=-self.compressed_length, stop=0,
                                           step=self.compressed_length / self.slab_element_count)

        angular_coordinates = [-np.arcsin(horizontal_coordinate / self.roll_pass.roll.working_radius) for
                               horizontal_coordinate in horizontal_coordinates]
        return angular_coordinates

    def flow_stress_along_roll_gap(self):
        pass

    def normal_pressure_at_plastic_entry(self):
        pass

    def normal_pressure(self):
        pass
