import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOCKER = shutil.which("docker")


@pytest.mark.skipif(DOCKER is None, reason="docker not available")
class TestDockerfile:
    @pytest.fixture(scope="class")
    @classmethod
    def image(cls):
        tag = "nrsak-py:pytest"
        subprocess.run(
            ["docker", "build", "-t", tag, str(ROOT)],
            check=True,
            capture_output=True,
            text=True,
        )
        yield tag
        subprocess.run(["docker", "rmi", "-f", tag], check=False, capture_output=True)

    def test_build_and_function_list(self, image):
        out = subprocess.run(
            ["docker", "run", "--rm", image],
            check=False, capture_output=True,
            text=True,
        )
        assert out.returncode == 0, out.stderr
        assert "nrSummary" in out.stdout

    def test_run_nr_summary_without_key_fails(self, image):
        out = subprocess.run(
            ["docker", "run", "--rm", image, "nrSummary"],
            check=False, capture_output=True,
            text=True,
        )
        assert out.returncode != 0
        combined = (out.stdout + out.stderr)
        assert "NR_KEY" in combined

    def test_runs_as_non_root(self, image):
        out = subprocess.run(
            ["docker", "run", "--rm", "--entrypoint", "id", image],
            check=False, capture_output=True,
            text=True,
        )
        assert out.returncode == 0
        assert "uid=0(root)" not in out.stdout
