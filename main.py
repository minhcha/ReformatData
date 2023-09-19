# Setting:
#   Have to paste test.robot file to save_path before run the code
#   Input some required paths into variables below

# Still not cover yet:
#   There are more than 1 line of expected data
#   Comment tag   =>   Had coded to cover it but not work
#   If there is exception when you run the code, you have to:
#       1. Delete all data in save_path but test.robot file and run from the beginning
#       or
#       2. Change data in load file to save your time
#   This bug appears some time in different place, Still don't know the reason
#       PermissionError: [WinError 32]
#       The process cannot access the file because it is being used by another process:
#       'C:/TestData/C128_SubsetC_FNC1_Pos_4_7Chars.bmp'
#       'C:/TestData/UPCA_PW4.bmp'
#       'C:/TestData/EAN8_P2.bmp'
#   =>  Maybe because of the work of another app ???

import os
import shutil
import array
import xml.etree.ElementTree as ET

# Variable

# Required path
file_load_path = "C:/VL_EVL/vl_test_tool_config/Test_Suite/Function/VL5.load"
# Folder that used to save data
test_result_path = "C:/TestData/"
# Place that save vlc file and itc file
vlc_itc_path = "C:/VL_EVL/vl_test_tool_config/"
# Image folder
image_origin_path = "//dl44h0lb3/IP-TECH/"
# Robo file path
robo_path = "C:/TestData/test.robot"

# Global variable:
# Address of sym folder
symbology_path = ""
# Address of test type folder
testtype_path = ""
# Address of testcase folder
TCID_path = ""


# To delete special character
def reformat_folder_name(folder_name):
    temp_name = ""
    for char in folder_name:
        if char.isalnum():
            temp_name = temp_name + char
    return temp_name


tree = ET.parse(file_load_path)
root = tree.getroot()

for symbology_content in root:
    sym_name = symbology_content.text.strip()
    symbology_path = test_result_path + sym_name
    os.makedirs(symbology_path)
    symbology_path = symbology_path + "/"
    print("Symbology: ", sym_name)

    for testtype_content in symbology_content:
        type_name = testtype_content.text.strip()
        type_name = reformat_folder_name(type_name)
        testtype_path = symbology_path + type_name
        os.makedirs(testtype_path)
        testtype_path = testtype_path + "/"
        print("Test type: ", type_name)

        for testcase_content in testtype_content:
            testcase_id = testcase_content.find('ExpectResultID').text
            TCID_path = testtype_path + testcase_id
            os.makedirs(TCID_path)
            print("Testcase ID: ", testcase_id)

            robo_path_des = TCID_path + "/test.robot"
            shutil.copy(robo_path, robo_path_des)

            vlc_path = testcase_content.find('VLC_Path').text.replace("\\", "/")
            vlc_sou = vlc_itc_path + vlc_path
            vlc_des = TCID_path + "/" + testcase_id + ".vlc"
            shutil.copy(vlc_sou, vlc_des)

            itc_path = testcase_content.find('Img_Path').text.replace("\\", "/")
            itc_sou = vlc_itc_path + itc_path
            itc_file = ET.parse(itc_sou)
            read_itc_file = itc_file.getroot()
            print("Path of itc file", itc_sou)

            csv_path = TCID_path + "/" + testcase_id + "set.csv"
            csv = open(csv_path, "w")
            csv_data = "No,Image,Content\n"
            csv.write(csv_data)

            for itc_symbology_content in read_itc_file:
                image_path = itc_symbology_content.text.strip()
                image_path = image_path.replace("\\", "/")
                image_sou = image_origin_path + image_path
                image_name = os.path.basename(image_sou)
                image_des = TCID_path + "/" + image_name
                shutil.copy(image_sou, image_des)
                print("Copy image ", image_name, "success")

                continue_flag = itc_symbology_content.find("expected_data")
                if continue_flag is None:
                    continue

                expected_data = itc_symbology_content.find("expected_data").text
                if itc_symbology_content.find("expected_data").text is None:
                    expected_data = '""'
                else:
                    expected_data = '"' + expected_data + '"'
                csv_data = "0," + image_name + "," + expected_data + "\n"
                csv.write(csv_data)
                print("Write data ", csv_data, " success ")

            csv.close()
