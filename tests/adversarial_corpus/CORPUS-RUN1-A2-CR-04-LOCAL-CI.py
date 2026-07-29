"""Lock alias: CR-04 environment checks live in the carrier corpus."""

from pathlib import Path


def test_cr04_local_ci_lock_is_present():
    assert (Path(__file__).with_name("CORPUS-RUN1-A2-CR-04.py")).is_file()
