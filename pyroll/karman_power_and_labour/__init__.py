import importlib.util
from . import roll_pass
from pyroll.core import config as _config

VERSION = "2.1.0"


@_config("PYROLL_EQUIVALENT_KARMAN_MODEL")
class Config:
    SHEAR_STRESS_DIRECTION_REGULARISATION = 0.001
    SHEAR_STRESS_PRESSURE_REGULARISATION = 0.001


REPORT_INSTALLED = bool(importlib.util.find_spec("pyroll.report"))

if REPORT_INSTALLED:
    from . import report
    import pyroll.report

    pyroll.report.plugin_manager.register(report)
