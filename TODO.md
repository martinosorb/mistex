- Currently tex2pdf does not work with files that don't end in .tex
- footnote / biblio stuff requires tests
- line break, is it dealt with correctly?
- test on windows
- filetype detection is bad. There should be a flag. Deactivation of \& unescaping
  should be optional on md-only. Can also escape latex in that mode.

Priority:
- Single line \[ \] match does not work. This is actually necessary and is
the last thing missing for the thesis to run.
