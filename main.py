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

# Variable

# Required path
file_load_path = "C:/VL_EVL/vl_test_tool_config/Test_Suite/Function/VL5.load"
# Folder that used to save data
save_path = "C:/TestData/"
# A temp place to save vlc file
vlc_temp = save_path + "config.vlc"
# Place that save vlc file and itc file
vlc_itc_path = "C:/VL_EVL/vl_test_tool_config/"
# Have to paste the test.robot file to save path before run the code
test_robot_path = save_path + "test.robot"
# Image folder
image_origin_path = "//dl44h0lb3/IP-TECH"

# Global variable:
# Address of sym folder
address_level_1 = ""
# Address of test type folder
address_level_2 = ""
# Address of testcase folder
address_level_3 = ""
# List of image will be read in itc file
image_list = [1, 3.5, "Hello"]


def create_folder(folder_name, father_address):
    print(folder_name)
    address = father_address + folder_name
    os.makedirs(address)
    print("Created folder: ", address)
    return address


def copy_test_robot(path):
    shutil.copy(test_robot_path, path)


# To delete special character
def reformat_folder_name(folder_name):
    temp_name = ""
    for char in folder_name:
        if char.isalnum():
            temp_name = temp_name + char
    return temp_name


# Open file load
with open(file_load_path, mode='r', encoding='utf-8') as f:
    # Read data
    data_in_line = f.readline()

    # Delete " " from data
    data_in_line = data_in_line.strip()

    # Stop flag for while loop
    stop = 0

    while stop != 1:

        # Find sym tag
        found_sym = data_in_line.find("<symbology>")

        # If there is sym tag in the line
        if found_sym != -1:
            # Clear sym tag
            data_in_line = data_in_line.strip("<symbology>")
            # Change " " to "_"
            data_in_line = data_in_line.replace(" ", "_")
            # Create grand folder of Sym
            address_level_1 = create_folder(data_in_line, save_path)
            address_level_1 = address_level_1 + "/"
            print("Test sym: ", data_in_line)

        # Find Test Type tag
        found_type = data_in_line.find("<Test_Type>")

        # If there is a test type tag
        if found_type != -1:
            # Delete Test Type tag
            data_in_line = data_in_line.replace("<Test_Type>", "")
            # If there is special character in Test Type, delete it
            if not data_in_line.isalnum():
                data_in_line = reformat_folder_name(data_in_line)

            # Create father folder with the name is test type
            address_level_2 = create_folder(data_in_line, address_level_1)
            address_level_2 = address_level_2 + "/"
            print("Test type: ", data_in_line)

        # Find ExpectResultID tag
        found_id = data_in_line.find("<ExpectResultID>")

        # If there is a ExpectResultID tag
        if found_id != -1:
            # Delete ExpectResultID open tag
            data_in_line = data_in_line[16:]
            # Delete ExpectResultID close tag
            data_in_line = data_in_line.replace("</ExpectResultID>", "")
            # Change " " to "_"
            data_in_line = data_in_line.replace(" ", "_")
            # Create test case folder with name is ExpectResultID
            address_level_3 = create_folder(data_in_line, address_level_2)

            # Copy vlc file to testcase folder
            vlc_new_path = address_level_3 + "/" + data_in_line + ".vlc"
            shutil.copy(vlc_temp, vlc_new_path)
            os.remove(vlc_temp)

            # Copy robo file to testcase folder
            robo_path = address_level_3 + "/test.robot"
            copy_test_robot(robo_path)
            print("Test case: ", data_in_line)

            # Image_list is list of image name that read from itc file
            for x in image_list:
                copy_flag = 0
                image_path = address_level_3 + "/" + x
                image_temp_path = save_path + x
                list_file = os.listdir(save_path)
                # If the image is already in temp folder, copy flag = 1
                for y in list_file:
                    if y == x:
                        copy_flag = 1
                # If copy flag = 1, copy image file to testcase folder
                if copy_flag == 1:
                    shutil.move(image_temp_path, image_path)
                    print("Move file ", x, " success")
                # Announce that the image is already in side the testcase folder
                else:
                    print("----- itc file contain 2 ", x, ", check in ", address_level_3, "-----")

            # Copy csv file to test case folder
            csv_path_temp = save_path + "set.csv"
            csv_path = address_level_3 + "/" + data_in_line + "set.csv"
            shutil.copy(csv_path_temp, csv_path)
            print("Create csv file success")
            os.remove(csv_path_temp)

        # Find VLC_Path tag
        found_vlc = data_in_line.find("<VLC_Path>")
        # If there is VLC_Path
        if found_vlc != -1:
            # Delete open tag and close tag
            data_in_line = data_in_line.strip("<VLC_Path>")
            data_in_line = data_in_line.strip("</VLC_Path>")
            # vlc path temp is the absolute path to vlc folder in load file
            vlc_path_temp = vlc_itc_path + data_in_line
            vlc_path_temp = vlc_path_temp.replace("\\", "/")
            # Copy it to temp folder
            shutil.copy(vlc_path_temp, vlc_temp)
            print("Copied vlc file to ", vlc_path_temp)

        # Find Img_Path tag
        found_itc = data_in_line.find("<Img_Path>")
        # If there is Img_Path
        if found_itc != -1:
            # Delete open tag and close tag
            data_in_line = data_in_line.strip("<Img_Path>")
            data_in_line = data_in_line.strip("</Img_Path>")

            # itc_path_temp is the absolute path to itc file that written in load file
            itc_path_temp = vlc_itc_path + data_in_line
            itc_path_temp = itc_path_temp.replace("\\", "/")

            # open itc file to read
            with open(itc_path_temp, mode='r', encoding='utf-8') as itc:
                itc_data_in_line = itc.readline()

                # Delete " "
                itc_data_in_line = itc_data_in_line.strip()

                # This is the flag stop to read itc file
                stop_itc = -1

                # Clear the list of image
                image_list.clear()

                # Create a .csv file to write
                csv_path = save_path + "set.csv"
                csv = open(csv_path, "w")
                csv_data_temp = "No, Image, Content \n"
                csv.write(csv_data_temp)

                while stop_itc == -1:

                    # Find comment tag and disable all of it -- still not work
                    found_start_comment = itc_data_in_line.find("<!--")
                    itc_data_in_line = itc_data_in_line.replace("<!--", "")
                    if found_start_comment != -1:
                        found_stop_comment = itc_data_in_line.find("-->")
                        while found_stop_comment == -1:
                            itc_data_in_line = itc.readline()
                            itc_data_in_line = itc_data_in_line.strip()

                    # Find image tag
                    found_image = itc_data_in_line.find("<Image>")
                    # If there is image tag
                    if found_image != -1:
                        # Delete image tag
                        image_path_temp = itc_data_in_line.replace("<Image>", "")
                        # Read the path of image
                        image_path = image_origin_path + "/" + image_path_temp
                        image_path = image_path.replace("\\", "/")
                        basename = os.path.basename(image_path)
                        image_new_path = save_path + basename
                        # Copy image to temp folder
                        shutil.copy(image_path, image_new_path)
                        image_list.append(basename)
                        # Write No. and image name to a temp variable
                        csv_data_temp = '0, ' + basename + ', '

                    # Find expected_data tag
                    found_expected_data = itc_data_in_line.find("<expected_data>")
                    # If there is expected_data tag
                    if found_expected_data != -1:
                        # Delete expected_data tag
                        expected_data = itc_data_in_line.replace("<expected_data>", "")
                        # Add "" to the beginning and the end of expected date
                        expected_data = '"' + expected_data + '"'
                        # Add it to temp variable
                        csv_data_temp = csv_data_temp + expected_data + ' \n'
                        # Write data from temp variable to csv file
                        csv.write(csv_data_temp)

                    # Read the next line of itc file
                    itc_data_in_line = itc.readline()
                    # Delete " "
                    itc_data_in_line = itc_data_in_line.strip()
                    # Find stop tag
                    stop_itc = itc_data_in_line.find("</Img_config>")
                # Close csv file
                csv.close()

        # Read the next line of load file
        data_in_line = f.readline()
        temp = data_in_line.find("</VLUTT_Config>")
        if temp != -1:
            stop = 1
        data_in_line = data_in_line.strip()
