# Minimal makefile for Sphinx documentation
# make html
# sphinx-build -b latex . _build/latex
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = ffs
SOURCEDIR     = .
BUILDDIR      = _build
#BUILDDIR    = ../../ffs-docs
PDFBUILDDIR = _build 
PDF     = ../manual.pdf

latexpdf: 
    $(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(PDFBUILDDIR)/latex 
    @echo "Running LaTeX files through pdflatex..." 
    make -C $(PDFBUILDDIR)/latex all-pdf 
    cp $(PDFBUILDDIR)/latex/*.pdf $(PDF) 
    @echo "pdflatex finished; see $(PDF)"
    
# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)