PDF_DIR = pdfs
TEX_NAME ?= resume.tex
TEX_BASENAME = $(basename $(TEX_NAME))
PDFBASENAME ?= output  # Default base name if not provided

# public_info parameters
PUBLIC_INFO_OPTIONA ?= X
PUBLIC_INFO_OPTIONB ?= X
PUBLIC_INFO_NAME ?= Student
PUBLIC_INFO_ID ?= 1234567
PUBLIC_INFO_DATE ?= N/A
PUBLIC_INFO_SIGNATURE ?=

# early_withdrawal parameters
STEP1_OPTION1 ?= X
STEP1_OPTION2 ?= X
STEP1_DROP1 ?= X
STEP1_DROP2 ?= X
STEP1_DROP3 ?= X
STEP1_OPTION3 ?= X

STEP2_MONTH ?= 01
STEP2_DAY ?= 01
STEP2_YEAR ?= 2001
STEP2_OPTION1 ?= X
STEP2_OPTION2 ?= X

STEP3_OPTION1 ?= X
STEP3_DATE ?= N/A
STEP3_OPTION2 ?= X

EARLY_WITHDRAWAL_NAME ?= Student
EARLY_WITHDRAWAL_ID ?= 1234567
EARLY_WITHDRAWAL_DATE ?= N/A
EARLY_WITHDRAWAL_SIGNATURE ?=

# ========= BUILD PUBLIC INFO =============
buildPublicInfo: $(TEX_NAME)
	@echo "Running pdflatex for buildPublicInfo..."
	[ -d $(PDF_DIR) ] || mkdir -p $(PDF_DIR)
	[ -f $(PDF_DIR)/$(PDFBASENAME).pdf ] && rm -f $(PDF_DIR)/$(PDFBASENAME).pdf || true
	echo "\
	\def\VAROPTIONA{$(PUBLIC_INFO_OPTIONA)}\
	\def\VAROPTIONB{$(PUBLIC_INFO_OPTIONB)}\
	\def\VARNAME{$(PUBLIC_INFO_NAME)}\
	\def\VARID{$(PUBLIC_INFO_ID)}\
	\def\VARDATE{$(PUBLIC_INFO_DATE)}\
	\def\VARSIGNATURE{$(PUBLIC_INFO_SIGNATURE)}\
	\input{$(TEX_NAME)}" | pdflatex -interaction=nonstopmode -output-directory=$(PDF_DIR) -jobname=$(PDFBASENAME)

# ========= BUILD EARLY WITHDRAWAL =============
buildEarlyWithdrawal: $(TEX_NAME)
	@echo "Running pdflatex for buildEarlyWithdrawal..."
	[ -d $(PDF_DIR) ] || mkdir -p $(PDF_DIR)
	[ -f $(PDF_DIR)/$(PDFBASENAME).pdf ] && rm -f $(PDF_DIR)/$(PDFBASENAME).pdf || true
	echo "\
	\def\VARNAME{$(EARLY_WITHDRAWAL_NAME)}\
	\def\VARID{$(EARLY_WITHDRAWAL_ID)}\
	\def\VARDATE{$(EARLY_WITHDRAWAL_DATE)}\
	\def\SoneOone{$(STEP1_OPTION1)}\
	\def\SoneOtwo{$(STEP1_OPTION2)}\
	\def\SoneDone{$(STEP1_DROP1)}\
	\def\SoneDtwo{$(STEP1_DROP2)}\
	\def\SoneDthree{$(STEP1_DROP3)}\
	\def\SoneOthree{$(STEP1_OPTION3)}\
	\def\StwoMonth{$(STEP2_MONTH)}\
	\def\StwoDay{$(STEP2_DAY)}\
	\def\StwoYear{$(STEP2_YEAR)}\
	\def\StwoOone{$(STEP2_OPTION1)}\
	\def\StwoOtwo{$(STEP2_OPTION2)}\
	\def\SthreeOone{$(STEP3_OPTION1)}\
	\def\SthreeDate{$(STEP3_DATE)}\
	\def\SthreeOtwo{$(STEP3_OPTION2)}\
	\def\VARSIGNATURE{$(EARLY_WITHDRAWAL_SIGNATURE)}\
	\input{$(TEX_NAME)}" | pdflatex -interaction=nonstopmode -output-directory=$(PDF_DIR) -jobname=$(PDFBASENAME)

# ========= CLEAN =============
clean:
	rm -f $(PDF_DIR)/*.aux $(PDF_DIR)/*.log $(PDF_DIR)/*.out $(PDF_DIR)/*.pdf
