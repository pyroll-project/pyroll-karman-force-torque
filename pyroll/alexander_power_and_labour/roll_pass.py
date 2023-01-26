import numpy as np
from pyroll.core import RollPass, Hook


@RollPass.extension_class
class RollPassExt(RollPass):
    coulomb_friction_coefficient = Hook[float]()
    """Friction coefficient according to Coulombs model."""


@RollPassExt.coulomb_friction_coefficient
def coulomb_friction_coefficient(self: RollPassExt):
    raise ValueError(
        "You must provide Coulomb's friction coefficient to use the pyroll-alexander-power-and-labour plugin.")


@RollPassExt.mean_front_tension
def mean_front_tension(self: RollPass):
    raise ValueError(
        "You must provide a mean front tension to use the pyroll-alexander-power-and-labour plugin.")


@RollPassExt.mean_back_tension
def mean_back_tension(self: RollPass):
    raise ValueError(
        "You must provide a mean back tension to use the pyroll-alexander-power-and-labour plugin.")
