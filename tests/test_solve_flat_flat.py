import logging
import webbrowser
from pathlib import Path

import numpy as np

from pyroll.core import Profile, PassSequence, RollPass, Roll, FlatGroove

DISK_ELEMENT_COUNT = 50


def test_solve_flat_flat(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

    import pyroll.freiberg_flow_stress
    import pyroll.interface_friction
    import pyroll.pillar_model
    import pyroll.local_velocity
    import pyroll.karman_power_and_labour

    in_profile = Profile.box(
        height=8e-3,
        width=100e-3,
        temperature=1200 + 273.15,
        strain=0,
        pillar_strains=np.zeros(pyroll.pillar_model.Config.PILLAR_COUNT),
        material=["C45", "steel"],
        density=7.5e3,
        specific_heat_capacity=690,
    )

    sequence = PassSequence(
        [
            RollPass(
                label="Flat",
                roll=Roll(
                    groove=FlatGroove(
                        usable_width=150e-3,
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                    neutral_point=-10e-3
                ),
                in_profile_rotation=0,
                gap=6e-3,
                back_tension=0,
                front_tension=0,
                disk_element_count=DISK_ELEMENT_COUNT,
                friction_factor=0.8
            ),

        ]
    )

    try:
        sequence.solve(in_profile)
    finally:
        print("\nLog:")
        print(caplog.text)

    try:
        import pyroll.report

        report = pyroll.report.report(sequence)

        report_file = tmp_path / "report.html"
        report_file.write_text(report)
        print(report_file)
        webbrowser.open(report_file.as_uri())

    except ImportError:
        pass
