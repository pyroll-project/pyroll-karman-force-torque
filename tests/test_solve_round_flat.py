import logging
import webbrowser
from pathlib import Path
import numpy as np

from pyroll.core import Profile, PassSequence, RollPass, Roll, FlatGroove

DISK_ELEMENT_COUNT = 30


def test_solve_round_flat(tmp_path: Path, caplog):
    caplog.set_level(logging.INFO, logger="pyroll")

    import pyroll.freiberg_flow_stress
    import pyroll.interface_friction
    import pyroll.pillar_model
    import pyroll.local_velocity
    import pyroll.karman_power_and_labour

    in_profile = Profile.round(
        diameter=19.5e-3,
        temperature=1200 + 273.15,
        strain=0,
        pillar_strains=np.zeros(pyroll.pillar_model.Config.PILLAR_COUNT),
        material=["C45", "steel"],
        flow_stress=100e6,
        density=7.5e3,
        specific_heat_capcity=690,
    )

    sequence = PassSequence(
        [
            RollPass(
                label="Flat",
                roll=Roll(
                    groove=FlatGroove(
                        usable_width=40e-3,
                    ),
                    nominal_radius=160e-3,
                    rotational_frequency=1,
                    neutral_point=-20e-3
                ),
                gap=10e-3,
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
        from pyroll.report import report

        report = report(sequence)
        f = tmp_path / "report.html"
        f.write_text(report)
        webbrowser.open(f.as_uri())

    except ImportError:
        pass
