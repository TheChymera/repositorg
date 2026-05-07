import subprocess
import pytest

def run_cli(*args, input=None):
    """Helper to invoke your CLI and return CompletedProcess."""
    result = subprocess.run(
        ["repositorg", *args],
        input=input,
        capture_output=True,
        text=True,
    )
    return result

def test_error_path():
    r = run_cli("--bad-flag")
    assert r.returncode != 0
    assert "error" in r.stderr.lower()

def test_reposit():
    r = run_cli(
        "reposit",
        "--no-ask",
        "--in-regex", r'^(?P<subject>.+?)_(?P<slice>.+?)_(?P<zoom>[0-9]+?)x_w[1-9]*(?P<modality>.+?)( .*)?\.(?P<extension>.+?)$',
        "--out-string", "sub-{subject}/sub-{subject}_slice-{slice!l}_zoom-{zoom}_{modality!l}.{extension!l}",
        "example_data/source_b/",
        "/tmp/repositorg"
        )
    print("CMD:", " ".join(r.args))
    print(r.stdout)
