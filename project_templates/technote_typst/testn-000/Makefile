DOCNAME = TESTN-000

TEMPLATE_VERSION = 0.1.0
PACKAGE_DIR = .typst-packages/preview/rubin-technote/$(TEMPLATE_VERSION)
LSST_TEXMF_REF ?= main
BIB_FILES = lsst.bib lsst-dm.bib refs.bib refs_ads.bib books.bib

# The git state is stamped into the document's front matter.
GITVERSION := $(shell git log -1 --date=short --pretty=%h)
GITSTATUS := $(shell git status --porcelain)
ifneq "$(GITSTATUS)" ""
	GITDIRTY = -dirty
endif

# Enforced PDF standards: archival (PDF/A-2a) and accessible (PDF/UA-1)
# output, making missing alt text a compilation failure. Set PDF_STANDARD
# to empty to explicitly opt out of the enforcement.
PDF_STANDARD ?= a-2a,ua-1

.PHONY:
init:
	pip install tox pre-commit
	pre-commit install

.PHONY:
pdf: $(PACKAGE_DIR) lsstbib
	typst compile --root . \
	  --package-path .typst-packages \
	  --font-path $(PACKAGE_DIR)/fonts \
	  --input source-version=$(GITVERSION)$(GITDIRTY) \
	  $(if $(PDF_STANDARD),--pdf-standard $(PDF_STANDARD)) \
	  index.typ $(DOCNAME).pdf

# Fetch the rubin-technote Typst template as a vendored package. Set
# LSST_TEXMF_DIR to copy it from a local lsst-texmf checkout instead of
# downloading it from GitHub.
$(PACKAGE_DIR):
	mkdir -p $(PACKAGE_DIR)
ifdef LSST_TEXMF_DIR
	cp -R $(LSST_TEXMF_DIR)/typst-lsstdoc/. $(PACKAGE_DIR)
else
	mkdir -p .typst-tmp
	curl -fsSL https://github.com/lsst/lsst-texmf/archive/refs/heads/$(LSST_TEXMF_REF).tar.gz \
	  | tar -xz -C .typst-tmp
	cp -R .typst-tmp/*/typst-lsstdoc/. $(PACKAGE_DIR)
	rm -rf .typst-tmp
endif

.PHONY:
template: $(PACKAGE_DIR)

lsstbib:
	mkdir -p lsstbib
	for bib in $(BIB_FILES); do \
	  curl -fsSL -o lsstbib/$$bib \
	    https://raw.githubusercontent.com/lsst/lsst-texmf/main/texmf/bibtex/bib/$$bib; \
	done

.PHONY:
sync-bibs:
	rm -rf lsstbib
	$(MAKE) lsstbib

.PHONY:
add-author:
	tox run -e add-author

.PHONY:
sync-authors:
	tox run -e sync-authors

.PHONY:
lint:
	tox run -e lint

.PHONY:
clean:
	rm -rf $(DOCNAME).pdf lsstbib .typst-packages .typst-tmp .tox
