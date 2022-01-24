import os
import pandas as pd
import json

path = r"E:\6025211018 - Swardiantara S\Drone Datasets\DJI_Mavic_Air\df048\2018_April\mobile_iOS_backup\df048\Export"

os.chdir(path)


def read_file(file_name):
    full_path = f"{path}/{file_name}"
    with open(full_path, 'r', encoding='utf-8') as file:
        # Extract the file contents here
        contents = file.read().strip()
        # f.close()
        # print(contents)
        first_char = contents[0]
        second_char = contents[1]
        # print(file_name, first_char, second_char)

        # if first_char == "{":
        #     n = 1
        #     print(n)
        #     n = n + 1
        #     # #     JSON
        #     # data = json.loads(f.read())
        #     # df = pd.json_normalize(data)
        #     # # df = pd.read_json(full_path)
        #     # df.to_csv(f"{path}/{file_name}.csv", index=False, encoding='utf-8')
        if first_char == "[" and second_char == "[":
            # Dictionary
            # string_value = "alphanumeric@123__"
            # s = ''.join(filter(str.isalnum, string_value))
            text_split = contents.split("],[")
            # print(text_split)
            record_list = []
            for record in text_split:
                # print(record)
                split_record = record.split(",")
                print(split_record)
                record = "".join(filter(str.isalnum, record))
                date = split_record[0].split(" ")[0].replace('[', "").replace('"', "")
                time = split_record[0].split(" ")[1].replace('"', "")
                message_type = split_record[1].replace('"', "")
                message = split_record[2].replace(']', "").replace('"', "")
                record_list.append([date, time, message_type, message])
                # print(record)
            dataframe = pd.DataFrame(record_list, index=None, columns=["date", "time", "message_type", "message"])
            dataframe.to_csv(f"{path}/{file_name}.csv", index=False, encoding='utf-8')
            # print(text_split)
        elif first_char == "[" and not second_char == "[":  # [2017-06-28 05:56:19.955]remove need upgrade groups
            # List
            # print(contents)
            lines = contents.split("\n")
            data_list = []
            for line in lines:
                text_split = line.split("]")
                # print(line)
                date = text_split[0].split(" ")[0].replace("[", "")
                time = text_split[0].split(" ")[1]
                message = text_split[1]
                data_list.append([date, time, message])
            dataframe = pd.DataFrame(data_list, index=None, columns=["date", "time", "message"])
            dataframe.to_csv(f"{path}/{file_name}.csv", index=False, encoding='utf-8')
        # print(f.read())
        file.close()


for files in os.listdir():
    # file_path = f"{path}\{file}"
    read_file(files)
