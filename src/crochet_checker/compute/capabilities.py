"""Runtime compute capability detection.

The validator always works locally. Optional accelerators are detected but
never required for correctness.
"""

from __future__ import annotations

import importlib.util
import os
import platform
import shutil
from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class ComputeCapabilities:
    python_version: str
    platform: str
    cpu_count: int
    has_numpy: bool
    has_pillow: bool
    has_opencv: bool
    has_torch: bool
    has_cuda: bool
    has_ollama: bool
    has_docker: bool
    quantum_backend: str | None
    remote_hpc_configured: bool
    recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _installed(package: str) -> bool:
    return importlib.util.find_spec(package) is not None


def detect_compute() -> ComputeCapabilities:
    has_torch = _installed("torch")
    has_cuda = False

    if has_torch:
        try:
            import torch

            has_cuda = bool(torch.cuda.is_available())
        except Exception:
            has_cuda = False

    if shutil.which("ollama"):
        ollama = True
    else:
        ollama = False

    quantum_backend = None

    if _installed("qiskit"):
        quantum_backend = "qiskit-installed"
    elif _installed("cirq"):
        quantum_backend = "cirq-installed"

    remote_hpc = bool(
        os.environ.get("CROCHET_HPC_ENDPOINT")
        or os.environ.get("CROCHET_CLOUD_ENDPOINT")
    )

    if has_cuda:
        recommendation = "GPU acceleration available for simulations."
    elif _installed("numpy"):
        recommendation = "Use NumPy/CPU parallel simulation."
    else:
        recommendation = "Use deterministic standard-library CPU mode."

    return ComputeCapabilities(
        python_version=platform.python_version(),
        platform=platform.platform(),
        cpu_count=os.cpu_count() or 1,
        has_numpy=_installed("numpy"),
        has_pillow=_installed("PIL"),
        has_opencv=_installed("cv2"),
        has_torch=has_torch,
        has_cuda=has_cuda,
        has_ollama=ollama,
        has_docker=shutil.which("docker") is not None,
        quantum_backend=quantum_backend,
        remote_hpc_configured=remote_hpc,
        recommendation=recommendation,
    )
