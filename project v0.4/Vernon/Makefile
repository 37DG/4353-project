# Set default filename (change dynamically from Python)
TEX_FILE ?= petition
PDF_FILE = $(TEX_FILE).pdf

all: $(PDF_FILE)

$(PDF_FILE): $(TEX_FILE).tex
	pdflatex -interaction=nonstopmode $(TEX_FILE).tex

clean:
	rm -f *.aux *.log *.out *.toc $(PDF_FILE) $(TEX_FILE).tex $(TEX_FILE)_signature.png

view: $(PDF_FILE)
	@case "$$(uname)" in \
		Darwin) open $(PDF_FILE) ;; \
		Linux) xdg-open $(PDF_FILE) || gio open $(PDF_FILE) ;; \
		CYGWIN*|MINGW32*|MSYS*|MINGW*) cygstart $(PDF_FILE) || start $(PDF_FILE) ;; \
		*) echo "Unsupported OS"; exit 1 ;; \
	esac
