import os
import pandas as pd
import json

def read_file(path, file_name, folder_data):
    # file_name = "contoh.csv"
    full_path = f"{path}/{file_name}"
    file_ext = file_name.split(".")        
    file_ext = file_ext[1] if len(file_ext) > 1 else "" 
    drone_model = folder_data["drone"]
    dataset = folder_data["dataset"]
    controller = folder_data["controller"]
    # print("Ekstensi: %s" % file_ext)
    if file_ext == "csv":
        flight_log = ""
        first_line = ""
        first_col = ""
        sep = ""
        
        # read file first line
        with open(full_path, "r") as file:
            first_line = file.readline()
            first_col = first_line.split(',')
            file.close()
            
        print("num of line: ", len(first_line))
        if (first_col == "CUSTOM.date [local]"):
            print("masuk waras")
            flight_log = pd.read_csv(full_path, encoding="utf-8")
        else:
            print("masuk ndak waras")
            dataframe = []
            # read ulang file untuk ambil content
            with open(full_path) as file:
                for i, line in enumerate(file):
                    if i == 0: # First row should be column name
                        sep = line.rstrip()[-1]
                        # print(sep)
                        # print("first line:", line)
                    elif i > 0:
                        # print("second line: ", line)
                        line = line.rstrip().split(sep)
                        print(len(line))
                        dataframe.append(line.rstrip().split(sep))
                flight_log = pd.DataFrame(data=dataframe[1:], columns=dataframe[0])
                file.close()
#         flight_log = ""
#         with open(full_path, "r") as file:
#             first_line = file.readline()
#             first_col = first_line.split(',')
#             print("num of line: ", len(first_line))
#             sep = ""
#             if (first_col == "CUSTOM.date [local]"):
#                 print("masuk waras")
#                 flight_log = pd.read_csv(full_path, encoding="utf-8")
#             else:
#                 print("masuk ndak waras")
#                 dataframe = []
#                 for i, line in enumerate(file):
#                     if i == 0: # First row should be column name
#                         sep = line.rstrip()[-1]
#                         # print(sep)
#                         # print("first line:", line)
#                     elif i > 0:
#                         # print("second line: ", line)
#                         line = line.rstrip().split(sep)
#                         print(len(line))
#                         dataframe.append(line.rstrip().split(sep))
#                 flight_log = pd.DataFrame(data=dataframe[1:], columns=dataframe[0])
#             file.close()
        # CUSTOM.date [local]
        # CUSTOM.updateTime [local]
        # APP.message
        # APP.tip
        # APP.warning
        # print(flight_log)
        # Filter non empty message
        print(flight_log.shape)
        df_message = flight_log[flight_log.iloc[:, -3].notnull()]
        df_tip = flight_log[flight_log.iloc[:, -2].notnull()]
        df_warning = flight_log[flight_log.iloc[:, -1].notnull()]
        merged = pd.concat([df_message, df_tip, df_warning], ignore_index=True)
        remove_duplicate = merged.drop_duplicates()
        record_list = []
        for i in range (0, remove_duplicate.shape[0]):
            date = remove_duplicate.iloc[i, 0]
            time = remove_duplicate.iloc[i, 1]
            message = str(remove_duplicate.iloc[i, -3]).strip()
            tip = str(remove_duplicate.iloc[i, -2]).strip()
            warning = str(remove_duplicate.iloc[i, -1]).strip()
            if not message == "" and message != "nan":
                # message = str(remove_duplicate.iloc[i, -3]).strip()
                # print("message : {}, length: {}".format(message, len(message)))
                record_list.append([drone_model, dataset, controller, file_name, date, time, message])
            if not tip == "" and tip != "nan":
                # message = str(remove_duplicate.iloc[i, -2]).strip()
                # print("message : {}, length: {}".format(tip, len(tip)))
                record_list.append([drone_model, dataset, controller, file_name, date, time, tip])
            if not warning == "" and warning != "nan":
                # message = str(remove_duplicate.iloc[i, -1]).strip()
                # print("message : {}, length: {}".format(warning, len(warning)))
                record_list.append([drone_model, dataset, controller, file_name, date, time, warning])
        dataframe = pd.DataFrame(record_list, index=None, columns=["drone_model", "dataset", "controller", "source_file", "date", "time", "message"])
        file_name = "extracted_" + file_name
        dataframe.to_csv(f"{path}/{file_name}.csv", index=False, encoding='utf-8')
        print(dataframe.shape)
        return ""
    elif file_ext == "":
        # Extract the ERROR_POP_LOG file content
        with open(full_path, 'r', encoding='utf-8') as file:
            # Extract the file contents here
            # contents = file.read().strip()
            
            date = file_name
            record_list = []
            lines = file.readlines()
            message = ""
            time = ""
            for line in lines:
                word = line.split(" ")
                if len(word) < 3 and word[0] == "##":
                    time =  word[1].strip()
                    continue
                elif len(word) > 2 and word[0] == "##":
                    time = word[1].strip()
                    message = " ".join(word[2:]).strip()
                else:
                    message = " ".join(word).strip()
                if not message == "" and not time == "":
                    record_list.append([drone_model, dataset, controller, file_name, date, time, message])
                # print(record_list)
            dataframe = pd.DataFrame(record_list, index=None, columns=["drone_model", "dataset", "controller", "source_file", "date", "time", "message"])
            file_name = "extracted_" + file_name
            dataframe.to_csv(f"{path}/{file_name}.csv", index=False, encoding='utf-8')
            print(dataframe.shape)
            file.close()
        return ""

def main():
    # Paste the full path here
    path = r"E:\6025211018 - Swardiantara S\drone-timeline\DJI_Inspire_1\df010\2018_June\mobile_android"
    os.chdir(path)
    path_split = path.split("\\")
    controller = path_split[-1]
    df = path_split[-3]
    drone_make = path_split[-4]
    folder_data = {
        "controller": controller,
        "dataset": df,
        "drone": drone_make
    }
    # listFiles = os.listdir()
    for filename in os.listdir():
        # file_path = f"{path}\{file}"
        print("Extracting file: %s" % filename)
        read_file(path, filename, folder_data)
        print("Finish Extracting file: %s\n" % filename)

if __name__ == "__main__":
    main()
