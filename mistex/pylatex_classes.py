import pylatex as pl


class LatexList(pl.base_classes.Container):
    def __init__(self, *args, **kwargs):
        super(LatexList, self).__init__(*args, **kwargs)

    def dumps(self):
        return self.dumps_content()

    def __repr__(self):
        return self.dumps_content()


class Verbatim(pl.base_classes.Environment):
    content_separator = "\n"


class Minted(pl.base_classes.Environment):
    def __init__(self, lang, outputdir):
        super().__init__(arguments=lang)
        self.packages = [pl.package.Package(
            "minted", options=pl.NoEscape(f"outputdir={outputdir}")
        )]
        self.content_separator = "\n"  # no % after \begin{minted}

    def dumps(self, *args, **kwargs):
        # unfortunately an additional \n is needed because minted won't
        # tolerate % after \end{minted} for some reason.
        return super().dumps(*args, **kwargs) + "\n"


class Href(pl.base_classes.CommandBase):
    packages = [pl.package.Package('hyperref', options="breaklinks=true")]
