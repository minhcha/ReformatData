# Setting:
#   Have to paste test.robot file to test_result_path before run the code
#   Input some required paths into variables below

# Still not cover yet:
#   There are more than 1 line of expected data
#   Comment tag   =>   Had coded to cover it but not work
#   If there is exception when you run the code, you have to:
#       1. Delete all data in test_result_path but test.robot file and run from the beginning
#       or
#       2. Change data in load file to save your time
#   This bug appears some time in different place, Still don't know the reason
#       PermissionError: [WinError 32]
#       The process cannot access the file because it is being used by another process:
#       'C:/TestData/C128_testtype_contentsetC_FNC1_Pos_4_7Chars.bmp'
#       'C:/TestData/UPCA_PW4.bmp'
#       'C:/TestData/EAN8_P2.bmp'
#   =>  Maybe because of the work of another app ???