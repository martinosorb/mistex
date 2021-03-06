from pathlib import Path
import pytest
import subprocess

HERE = Path(__file__).resolve().parent
AUX_DIR = HERE / "other_files"
out_file = HERE / "out.pdf"
cachedir = HERE / "cache"

# check if the latexmk command exists in the system
latexmk_not_available = subprocess.call("type latex > /dev/null", shell=True)


def test_import():
    from mistex import tex2pdf
    tex2pdf


@pytest.mark.skipif(latexmk_not_available, reason="latexmk not installed")
def test_compile():
    from mistex import tex2pdf
    assert not out_file.exists()
    tex2pdf(
        AUX_DIR / "invariant.tex",
        out_file,
        cachedir,
    )

    # check the output file has been created
    assert out_file.exists()
    out_file.unlink()  # clean up
    # check there are no compilation files around
    assert len(list(HERE.glob("*.aux"))) == 0
    # check there are files in the cache dir
    assert len(list(cachedir.glob("*.aux"))) == 1
    [f.unlink() for f in cachedir.glob("*")]  # clean up
    cachedir.rmdir()
