PDF_DIR = pdfs
PDF_NAME = $(PDF_DIR)/resume.pdf
TEX_NAME = resume.tex

# Default GPA (can be overwritten when calling make)
GPA ?= 4.0  

all: $(PDF_NAME)

$(PDF_NAME): $(TEX_NAME)
	if not exist $(PDF_DIR) mkdir $(PDF_DIR)
	pdflatex -interaction=nonstopmode -output-directory=$(PDF_DIR) "\def\gpa{$(GPA)}\input{$(TEX_NAME)}"

clean:
	if exist $(PDF_DIR) del /Q $(PDF_DIR)\*.aux $(PDF_DIR)\*.log $(PDF_DIR)\*.out $(PDF_DIR)\*.pdf
