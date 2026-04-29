MAIN = report_latex
BIB = references
IMAGES = $(wildcard images/*)

.PHONY:all clean open pdf

all: pdf 

pdf: $(BIB).bib $(MAIN).tex $(IMAGES)
	pdflatex $(MAIN).tex
	bibtex $(MAIN)
	pdflatex $(MAIN).tex
	pdflatex $(MAIN).tex

partial: $(MAIN).tex $(IMAGES)
	pdflatex $(MAIN).tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc $(MAIN).pdf

open:
	xdg-open $(MAIN).pdf