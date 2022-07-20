import os
import csv

def read_file(path, file_name, folder_data):
    # file_name = "contoh.csv"
    full_path = f"{path}/{file_name}"
    file_ext = file_name.split(".")        
    file_ext = file_ext[1] if len(file_ext) > 1 else "" 
    drone_model = folder_data["drone"]
    dataset = folder_data["dataset"]
    controller = folder_data["controller"]
    print("Ekstensi: %s" % file_ext)
    if file_ext == "csv":
        rows = csv.reader(full_path, delimiter=",")
        for row in rows:
            print(row)


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