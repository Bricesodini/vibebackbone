"""Corpus guard for RUN1-A2-03: exact mode rejects external run paths."""

import importlib.util
import sys
from pathlib import Path


def _gate():
    root = Path(__file__).resolve().parents[2]
    path = root / "tools" / "vbb-adversarial-gate.py"
    spec = importlib.util.spec_from_file_location("corpus_run1_gate", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_run1_a2_03_external_path_is_not_canonical_subject(tmp_path):
    gate = _gate()
    runs = tmp_path / "runs"
    runs.mkdir()
    external = tmp_path / "external" / "same-name"
    external.mkdir(parents=True)
    assert (
        gate.resolve_run_dir(
            external,
            runs_dir=runs,
            require_canonical_child=True,
        )
        is None
    )
