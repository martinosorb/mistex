import pylatex as pl


class LatexList(pl.base_classes.Container):
    def dumps(self):
        return self.dumps_content()


class Minted(pl.base_classes.Environment):
    packages = [pl.package.Package('minted')]
