PDF_DIR = pdfs
TEX_NAME ?= resume.tex
TEX_BASENAME = $(basename $(TEX_NAME))
PDFBASENAME ?= output  # Default base name if not provided

# public_info parameters
# A at Line 884, B at Line 962
PUBLIC_INFO_OPTIONA ?= X
PUBLIC_INFO_OPTIONB ?= X
# Line 1022
PUBLIC_INFO_NAME ?= Student
# Line 1048
PUBLIC_INFO_ID ?= 1234567
# Line 1056
PUBLIC_INFO_DATE ?= N/A
# Line 1040
#PUBLIC_INFO_SIGNATURE ?= C:/Users/jtzhu/Desktop/software design project2.0/project2.1/media/Jinting_Zhu_PublicInfo.jpeg

########################################
# early_withdrawal parameters
# 668
STEP1_OPTION1 ?= X
# 676
STEP1_OPTION2 ?= X
# 741
STEP1_DROP1 ?= X
#751
STEP1_DROP2 ?= X
#792
STEP1_DROP3 ?= X
#806
STEP1_OPTION3 ?= X

#918
STEP2_MONTH ?= 01
#932
STEP2_DAY ?= 01
#959
STEP2_YEAR ?= 2001
# 1002
STEP2_OPTION1 ?= X
# 1014
STEP2_OPTION2 ?= X

# 1055
STEP3_OPTION1 ?= X
# 1066
STEP3_DATE ?= N/A
# 1109
STEP3_OPTION2 ?= X


# step4 options are in 1141 1156 1217

# step5 options are in 1292 1300 1368 1376 1384 1434 1446

# 263
EARLY_WITHDRAWAL_NAME ?= Student
# 339
EARLY_WITHDRAWAL_ID ?= 1234567
# 352
EARLY_WITHDRAWAL_DATE ?= N/A

# signture in 277


buildPublicInfo: $(TEX_NAME)
	if not exist $(PDF_DIR) mkdir $(PDF_DIR)
	if exist $(PDF_DIR)\$(PDFBASENAME).pdf del /Q $(PDF_DIR)\$(PDFBASENAME).pdf
	pdflatex -interaction=nonstopmode -output-directory=$(PDF_DIR)\
		"\def\VAROPTIONA{$(PUBLIC_INFO_OPTIONA)}\
		 \def\VAROPTIONB{$(PUBLIC_INFO_OPTIONB)}\
		 \def\VARNAME{$(PUBLIC_INFO_NAME)}\
		 \def\VARID{$(PUBLIC_INFO_ID)}\
		 \def\VARDATE{$(PUBLIC_INFO_DATE)}\
		 \def\VARSIGNATURE{$(PUBLIC_INFO_SIGNATURE)}\
		 \input{$(TEX_NAME)}"

	cd $(PDF_DIR) && rename $(TEX_BASENAME).pdf $(PDFBASENAME).pdf

buildEarlyWithdrawal: $(TEX_NAME)
	if not exist $(PDF_DIR) mkdir $(PDF_DIR)
	if exist $(PDF_DIR)\$(PDFBASENAME).pdf del /Q $(PDF_DIR)\$(PDFBASENAME).pdf
	pdflatex -interaction=nonstopmode -output-directory=$(PDF_DIR)\
		"\def\VARNAME{$(EARLY_WITHDRAWAL_NAME)}\
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
		 \input{$(TEX_NAME)}"
	
	cd $(PDF_DIR) && rename $(TEX_BASENAME).pdf $(PDFBASENAME).pdf

clean:
	if exist $(PDF_DIR) del /Q $(PDF_DIR)\*.aux $(PDF_DIR)\*.log $(PDF_DIR)\*.out
