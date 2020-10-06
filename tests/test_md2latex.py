from pathlib import Path
from mistex.core import read_file
import pytest

HERE = Path(__file__).resolve().parent
AUX_DIR = HERE / "other_files"

HEAD = """
\\documentclass{report}
\\date{}
\\begin{document}

"""
TAIL = "\n\\end{document}"


def test_import_instantiate():
    from mistex import md2latex
    md2latex()


def test_auto_no_add_header():
    from mistex import md2latex
    parse = md2latex()

    in_file = read_file(AUX_DIR / "invariant-tex")
    result = parse(in_file)
    assert result.strip("\n") == in_file.strip("\n")


def test_no_add_header():
    from mistex import md2latex
    parse = md2latex(filetype="tex")

    in_file = read_file(AUX_DIR / "plain-md")
    result = parse(in_file)
    assert result.strip("\n") == in_file.strip("\n")


def test_add_header():
    from mistex import md2latex
    parse = md2latex(filetype="md")
    in_file = read_file(AUX_DIR / "invariant-tex")
    result = parse(in_file)
    expected = HEAD + in_file + TAIL
    assert result.strip("\n") == expected.strip("\n")


def test_auto_add_header():
    from mistex import md2latex
    parse = md2latex()
    in_file = read_file(AUX_DIR / "plain-md")
    result = parse(in_file)
    expected = HEAD + in_file + TAIL
    assert result.strip("\n") == expected.strip("\n")


def test_error():
    from mistex import md2latex
    with pytest.raises(ValueError):
        md2latex(filetype="foobar")
