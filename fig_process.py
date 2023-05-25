import os
import csv


def makedir(dir_path):
    os.makedirs(dir_path, exist_ok=True)


def savefig(figure, metric, file_format):
    figure.savefig(metric + '.' + file_format, format=file_format)


def Print(file, per, date, file_name):
    print(file)
    dir_path = "metrics/" + file
    os.makedirs(dir_path, exist_ok=True)
    for i in range(len(per)):
        print(str(date[i]) + " : " + str(per[i]))
    with open(os.path.join(dir_path, file_name + ".csv"), "w", newline="") as csv_file:
        fieldnames = ["date", "number"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(per)):
            writer.writerow({"date": str(date[i]), "number": str(per[i])})