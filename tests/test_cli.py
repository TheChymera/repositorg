import pytest
import shlex
import subprocess

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

def test_reposit(example_data, tmp_path):
    r = run_cli(
        "reposit",
        "--no-ask",
        "--in-regex", r"^(?P<subject>.+?)_(?P<slice>.+?)_(?P<zoom>[0-9]+?)x_w[1-9]*(?P<modality>.+?)( .*)?\.(?P<extension>.+?)$",
        "--out-string", r"sub-{subject}/sub-{subject}_slice-{slice!l}_zoom-{zoom}_{modality!l}.{extension!l}",
        str(example_data / "source_b"),
        str(tmp_path),
        )
    print("\nRunning command:", " ".join(shlex.quote(a) for a in r.args))
    #print(r.stdout)
    # Check whether the correct output file names are constructed
    assert "sub-5700/sub-5700_slice-a4_zoom-5_egfp.tif" in r.stdout
    assert "sub-5700/sub-5700_slice-a4_zoom-5_dsred.tif" in r.stdout
    assert "sub-5700/sub-5700_slice-a4_zoom-5_transmission.tif" in r.stdout

    # Check there are no errors
    assert "not found" not in r.stdout
