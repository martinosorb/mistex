import pytest
from pathlib import Path

# find test files
HERE = Path(__file__).resolve().parent
IN_DIR = HERE / "in"
OUT_DIR = HERE / "out"


@pytest.fixture(params=IN_DIR.rglob("*"))
def load_in_out(request):
    fname = request.param.name
    with open(IN_DIR / fname) as file:
        in_file = file.read()
    with open(OUT_DIR / fname) as file:
        out_file = file.read()
    return in_file, out_file


def test_compare(load_in_out):
    in_file, out_file = load_in_out
    out_file = out_file.strip("\n")

    from mistex import md2latex
    parse = md2latex()
    result = parse(in_file).strip("\n")

    print("----- EXPECTED -----")
    print(out_file)
    print("----- OUTPUT -----")
    print(result)
    assert result == out_file
