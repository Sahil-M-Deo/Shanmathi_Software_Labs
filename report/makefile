MAIN = report
BIB = references
IMAGES = $(wildcard images/*)

.PHONY:all clean open partial

all: $(MAIN).pdf

$(MAIN).pdf: $(BIB).bib $(MAIN).tex $(IMAGES)
	pdflatex $(MAIN).tex
	bibtex $(MAIN)
	pdflatex $(MAIN).tex
	pdflatex $(MAIN).tex

partial:
	pdflatex $(MAIN).tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.run.xml *blx.bib

open:
	xdg-open $(MAIN).pdf
