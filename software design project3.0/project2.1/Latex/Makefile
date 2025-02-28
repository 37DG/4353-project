PDF_DIR = pdfs
TEX_NAME ?= resume.tex
TEX_BASENAME = $(basename $(TEX_NAME))
PDFBASENAME ?= output  # Default base name if not provided

# public_info parameters
# A at Line 884, B at Line 962
PUBLIC_INFO_OPTIONA ?= N/A
PUBLIC_INFO_OPTIONB ?= N/A
# Line 1022
PUBLIC_INFO_NAME ?= Student
# Line 1048
PUBLIC_INFO_ID ?= 1234567
# Line 1056
PUBLIC_INFO_DATE ?= 2021-01-01
# Line 1040
#PUBLIC_INFO_SIGNATURE ?= C:/Users/jtzhu/Desktop/software design project2.0/project2.1/media/Jinting_Zhu_PublicInfo.jpeg

buildPublicInfo: $(TEX_NAME)
	if not exist $(PDF_DIR) mkdir $(PDF_DIR)
	if exist $(PDF_DIR)\$(PDFBASENAME).pdf del /Q $(PDF_DIR)\$(PDFBASENAME).pdf
	pdflatex -interaction=nonstopmode -output-directory=$(PDF_DIR) "\def\VAROPTIONA{$(PUBLIC_INFO_OPTIONA)}\def\VAROPTIONB{$(PUBLIC_INFO_OPTIONB)}\def\VARNAME{$(PUBLIC_INFO_NAME)}\def\VARID{$(PUBLIC_INFO_ID)}\def\VARDATE{$(PUBLIC_INFO_DATE)}\def\VARSIGNATURE{$(PUBLIC_INFO_SIGNATURE)}\input{$(TEX_NAME)}"
	cd $(PDF_DIR) && rename $(TEX_BASENAME).pdf $(PDFBASENAME).pdf


clean:
	if exist $(PDF_DIR) del /Q $(PDF_DIR)\*.aux $(PDF_DIR)\*.log $(PDF_DIR)\*.out
