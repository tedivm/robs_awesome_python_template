# This file is deprecated by python in favor of setup.cfg
# However, some tools haven't caught up so we leave this here for them.
# All dependency and build configuration comes from setup.cfg.
# Other configuration, such as for linters, is in pyproject.toml.

import setuptools
import versioneer

setuptools.setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
