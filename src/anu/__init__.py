"""The hypermodern Python project."""
try:
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

from . import cli  # noqa
from . import data  # noqa

# from . import features  # noqa
# from . import metrics  # noqa

# from . import models  # noqa
# from . import parser  # noqa
# from . import pipelines  # noqa
# from . import visualization  # noqa
