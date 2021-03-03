- Currently tex2pdf does not work with files that don't end in .tex
- footnote / biblio stuff
- escape latex (create md only mode?)
- figure out what block error is and when link text is None by looking at parser; same for line break.
- test on windows
- remove add_header in renderer class (or use it)
- 'escape' in renderer class
- filetype detection is bad. There should be a flag. Deactivation of \& unescaping should be optional on md-only.

Priority:
- Bad things happen with double-backticks already present
- Single line \[ \] match does not work. This is actually necessary and is
the last thing missing for the thesis to run.
