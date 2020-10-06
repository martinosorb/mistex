import pytest
from pathlib import Path
from mistex.core import read_file

# find test files
HERE = Path(__file__).resolve().parent
IN_DIR = HERE / "in"
OUT_DIR = HERE / "out"
IN_FILES = [f.name for f in IN_DIR.rglob("*")]


@pytest.fixture(params=IN_FILES)
def load_in_out(request):
    fname = request.param
    in_file = read_file(IN_DIR / fname)
    out_file = read_file(OUT_DIR / fname)
    return in_file, out_file


def test_compare(load_in_out):
    in_file, out_file = load_in_out
    out_file = out_file.strip("\n")

    from mistex import md2latex
    parse = md2latex(filetype='md')
    result = parse(in_file).strip("\n")

    print("----- EXPECTED -----")
    print(out_file)
    print("----- OUTPUT -----")
    print(result)
    assert result == out_file
