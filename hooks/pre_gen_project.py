import re
import shutil
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

module_name = "{{ cookiecutter.__package_slug }}"

if not re.match(MODULE_REGEX, module_name):
    print("ERROR: %s is not a valid Python module name!" % module_name)
    # exits with status 1 to indicate failure
    sys.exit(1)

# Check if UV is installed
if not shutil.which("uv"):
    print("\n" + "=" * 80)
    print("ERROR: UV is not installed!")
    print("=" * 80)
    print("\nThis template requires UV for Python package management.")
    print("\nTo install UV, run one of the following commands:")
    print("\n  # On macOS and Linux:")
    print("  curl -LsSf https://astral.sh/uv/install.sh | sh")
    print("\n  # Using pip:")
    print("  pip install uv")
    print("\n  # Using pipx:")
    print("  pipx install uv")
    print("\n  # Using Homebrew:")
    print("  brew install uv")
    print("\nFor more installation options, visit: https://docs.astral.sh/uv/getting-started/installation/")
    print("\nAfter installing UV, you can regenerate this project using cookiecutter's replay feature:")
    print("  cookiecutter --replay gh:tedivm/robs_awesome_python_template")
    print("\nOr run the original cookiecutter command again.")
    print("=" * 80 + "\n")
    sys.exit(1)
