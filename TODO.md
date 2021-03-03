- Currently tex2pdf does not work with files that don't end in .tex
- footnote / biblio stuff
- figure out what block error is and when link text is None by looking at parser; same for line break.
- test on windows
- filetype detection is bad. There should be a flag. Deactivation of \& unescaping
  should be optional on md-only. can also escape latex.

Priority:
- Single line \[ \] match does not work. This is actually necessary and is
the last thing missing for the thesis to run.
