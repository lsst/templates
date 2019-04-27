DOCTYPE = {{ cookiecutter.series.upper() }}
DOCNUMBER = {{ cookiecutter.serial_number }}
DOCNAME = $(DOCTYPE)-$(DOCNUMBER)

tex = $(filter-out $(wildcard *acronyms.tex) , $(wildcard *.tex))

GITVERSION := $(shell git log -1 --date=short --pretty=%h)
GITDATE := $(shell git log -1 --date=short --pretty=%ad)
GITSTATUS := $(shell git status --porcelain)
ifneq "$(GITSTATUS)" ""
	GITDIRTY = -dirty
endif

TEXMFHOME = lsst-texmf/texmf

$(DOCNAME).pdf: $(tex)
	xelatex $(DOCNAME)
	bibtex $(DOCNAME)
	xelatex $(DOCNAME)
	bibtex $(DOCNAME)
	xelatex $(DOCNAME)
	xelatex $(DOCNAME)

acronyms.tex: $(tex) myacronyms.txt
	$(TEXMFHOME)/../bin/generateAcronyms.py $(tex)

.PHONY: clean
clean:
	rm -f $(DOCNAME).aux
	rm -f $(DOCNAME).bbl
	rm -f $(DOCNAME).blg
	rm -f $(DOCNAME).glg
	rm -f $(DOCNAME).glo
	rm -f $(DOCNAME).gls
	rm -f $(DOCNAME).ist
	rm -f $(DOCNAME).log
	rm -f $(DOCNAME).out
	rm -f $(DOCNAME).pdf
	rm -f $(DOCNAME).rec
	rm -f $(DOCNAME).toc
	rm -f meta.tex

.FORCE:

meta.tex: Makefile .FORCE
	rm -f $@
	touch $@
	echo '% GENERATED FILE -- edit this in the Makefile' >>$@
	/bin/echo '\newcommand{\lsstDocType}{$(DOCTYPE)}' >>$@
	/bin/echo '\newcommand{\lsstDocNum}{$(DOCNUMBER)}' >>$@
	/bin/echo '\newcommand{\vcsRevision}{$(GITVERSION)$(GITDIRTY)}' >>$@
	/bin/echo '\newcommand{\vcsDate}{$(GITDATE)}' >>$@
