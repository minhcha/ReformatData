import os
import shutil
import xml.etree.ElementTree as ET
import csv
import tkinter as tk
from tkinter import ttk, filedialog

# Global variable:
# Address of sym folder
symbology_path = ""
# Address of test type folder
test_type_path = ""
# Address of testcase folder
TCID_path = ""

#Read global variables from csv file
with open('global_vars.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        file_load_path = row[0]
        robo_path = row[1]
        test_result_path = row[2]
        vlc_itc_path = row[3]
        image_origin_path = row[4]

def choosefile_insertlabel(filepath, dialogname, label):
    filepath = filedialog.askopenfilename(title=dialogname)
    label.config(text=filepath)

def choosefolder_insertlabel(folderpath, dialogname, label):
    folderpath = filedialog.askdirectory(title=dialogname)
    label.config(text=folderpath + "/")

# To delete special character
def reformat_folder_name(folder_name):
    temp_name = ""
    for char in folder_name:
        if char.isalnum():
            temp_name = temp_name + char
    return temp_name

def run(file_load_path, robo_path, test_result_path, vlc_itc_path, image_origin_path):
    #Write global variables to csv file
    with open('global_vars.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([file_load_path, robo_path, test_result_path, vlc_itc_path, image_origin_path])

    tree = ET.parse(file_load_path)
    root = tree.getroot()

    for symbology_content in root:
        sym_name = symbology_content.text.strip()
        symbology_path = test_result_path + sym_name
        os.makedirs(symbology_path)
        print("Symbology: ", sym_name)

        for test_type_content in symbology_content:
            type_name = test_type_content.text.strip()
            type_name = reformat_folder_name(type_name)
            test_type_path = symbology_path + "/" + type_name
            os.makedirs(test_type_path)
            print("Test type: ", type_name)

            for testcase_content in test_type_content:
                testcase_id = testcase_content.find('ExpectResultID').text
                TCID_path = test_type_path + "/" + testcase_id
                os.makedirs(TCID_path)
                print("Testcase ID: ", testcase_id)

                robo_path_des = TCID_path + "/test.robot"
                shutil.copy(robo_path, robo_path_des)

                vlc_path = testcase_content.find('VLC_Path').text.replace("\\", "/")
                vlc_sou = vlc_itc_path + vlc_path
                vlc_name = os.path.basename(vlc_sou)
                vlc_des = TCID_path + "/" + vlc_name
                shutil.copy(vlc_sou, vlc_des)

                itc_path = testcase_content.find('Img_Path').text.replace("\\", "/")
                itc_sou = vlc_itc_path + itc_path
                itc_name = os.path.basename(itc_sou).replace(".itc", "")
                itc_file = ET.parse(itc_sou)
                read_itc_file = itc_file.getroot()
                print("Path of itc file", itc_sou)

                csv_path = TCID_path + "/" + itc_name + "_set.csv"
                csv_file = open(csv_path, "w", newline="")
                # csv_data = "No,Image,Content\n"
                writer_csv_file = csv.writer(csv_file)
                writer_csv_file.writerow(['No', 'Image', 'Content'])
                # csv_file.write(csv_data)

                for itc_symbology_content in read_itc_file:
                    image_path = itc_symbology_content.text.strip()
                    image_path = image_path.replace("\\", "/")
                    image_sou = image_origin_path + image_path
                    image_name = os.path.basename(image_sou)
                    image_des = TCID_path + "/" + image_name
                    shutil.copy(image_sou, image_des)
                    print("Copy image ", image_name, "success")
                    num = 0

                    continue_flag = itc_symbology_content.find("expected_data")
                    if continue_flag is None:
                        for image_option in itc_symbology_content:
                            for label_option in image_option:
                                expected_data = label_option.find("expected_data").text
                                if expected_data is None:
                                    expected_data = '""'
                                else:
                                    expected_data = '"' + expected_data + '"'
                                csv_data = str(num) + ',' + image_name + ',""' + expected_data + '"\n'
                                writer_csv_file.writerow([str(num), str(image_name), str(expected_data)])
                                # csv_file.write(csv_data)
                                print("Write data ", csv_data, " success ")
                                num = num + 1
                    else:
                        expected_data = itc_symbology_content.find("expected_data").text
                        if expected_data is None:
                            expected_data = '""'
                        else:
                            expected_data = '"' + expected_data + '"'
                        csv_data = '0,' + image_name + ',""' + expected_data + '"\n'
                        # csv_file.write(csv_data)
                        writer_csv_file.writerow([str(num), str(image_name), str(expected_data)])
                        print("Write data ", csv_data, " success ")

                csv_file.close()


# GUI
window = tk.Tk()
window.title("Convert TestSuite")
window.geometry("700x300")

file_load_button = tk.Button(window, text="Load File", command=lambda: choosefile_insertlabel(file_load_path, "Choose load file", file_load_label))
file_load_button.grid(row=0, column=0, sticky='w')
file_load_label = tk.Label(window, text=file_load_path, fg="blue")
file_load_label.grid(row=0, column=1, sticky='w')

file_robot_button = tk.Button(window, text="test.robot File", command=lambda: choosefile_insertlabel(robo_path, "Choose test.robot file", file_robot_label))
file_robot_button.grid(row=1, column=0, sticky='w')
file_robot_label = tk.Label(window, text=robo_path, fg="blue")
file_robot_label.grid(row=1, column=1, sticky='w')

folder_testresult_button = tk.Button(window, text="TestResult Folder", command=lambda: choosefolder_insertlabel(test_result_path, "Choose TestResult folder", folder_testresult_label))
folder_testresult_button.grid(row=2, column=0, sticky='w')
folder_testresult_label = tk.Label(window, text=test_result_path, fg="blue")
folder_testresult_label.grid(row=2, column=1, sticky='w')

folder_config_button = tk.Button(window, text="Config Folder", command=lambda: choosefolder_insertlabel(vlc_itc_path, "Choose config folder", folder_config_label))
folder_config_button.grid(row=3, column=0, sticky='w')
folder_config_label = tk.Label(window, text=vlc_itc_path, fg="blue")
folder_config_label.grid(row=3, column=1, sticky='w')

folder_originimage_button = tk.Button(window, text="Origin Image Folder", command=lambda: choosefolder_insertlabel(image_origin_path, "Choose origin image folder", folder_originimage_label))
folder_originimage_button.grid(row=4, column=0, sticky='w')
folder_originimage_label = tk.Label(window, text=image_origin_path, fg="blue")
folder_originimage_label.grid(row=4, column=1, sticky='w')

OK_button = tk.Button(window, text="OK", command=lambda: run(file_load_label.cget("text"), file_robot_label.cget("text"), folder_testresult_label.cget("text"), folder_config_label.cget("text"), folder_originimage_label.cget("text")))
OK_button.grid(row=5, column=1, sticky='w')

window.mainloop()