import pytest
import os

# find test files
HERE = os.path.dirname(os.path.abspath(__file__))
IN_DIR = os.path.join(HERE, "in")
OUT_DIR = os.path.join(HERE, "out")
IN_FILES = os.listdir(IN_DIR)
OUT_FILES = os.listdir(OUT_DIR)
assert len(IN_FILES) == len(OUT_FILES)


@pytest.fixture(params=IN_FILES)
def load_in_out(request):
    with open(os.path.join(IN_DIR, request.param)) as file:
        in_file = file.read()
    with open(os.path.join(OUT_DIR, request.param)) as file:
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
