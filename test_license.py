import subprocess
import pytest

# Define the path to your script
SCRIPT_PATH = "./license-validate.py"

def run_validator(argument):
    """Helper to run the script and return the exit code."""
    result = subprocess.run(
        [SCRIPT_PATH, argument],
        capture_output=True,
        text=True
    )
    return result.returncode

def test_license_validate_simple_success():
    exit_code = run_validator("GPL-2.0-or-later")
    assert exit_code == 0, f"Expected 0 but got {exit_code}"

def test_license_validate_and_success():
    exit_code = run_validator("Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0")
    assert exit_code == 0, f"Expected 0 but got {exit_code}"

def test_license_validate_complex_success():
    exit_code = run_validator("AGPL-3.0-only AND BSD-3-Clause AND 0BSD AND Apache-2.0 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0 AND (Unlicense OR MIT) AND (Zlib OR Apache-2.0 OR MIT) AND (ISC AND MIT AND OpenSSL)")
    assert exit_code == 0, f"Expected 0 but got {exit_code}"


def test_license_validate_failure_BSD3Clear_without_package():
    """Test that 'BAR' returns a non-zero exit code (Failure)."""
    exit_code = run_validator("BSD-3-Clause-Clear")
    assert exit_code != 0, f"Expected non-zero but got {exit_code}"

def test_license_validate_failure_BSD3_Clear():
    exit_code = run_validator("BSD-3-Clause-ClearSomeMoreNotValid")
    assert exit_code != 0, f"Expected non-zero but got {exit_code}"

def test_license_validate_failure_not_allowed():
    exit_code = run_validator("Frameworx-1.0")
    assert exit_code != 0, f"Expected non-zero but got {exit_code}"
