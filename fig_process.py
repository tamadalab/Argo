import matplotlib.pyplot as pyplot
import os
import csv

def makedir(dir_path):
    os.makedirs(dir_path, exist_ok=True)

def savefig(figure, metric, format):
    figure.savefig(metric + '.' + format, format = format)
    

def Print(file, per, date, file_name):
    print(file)
    dir_path = "metrics/"+file
    os.makedirs(dir_path, exist_ok=True)
    for i in range(len(per)):
        print(str(date[i]) + " : " + str(per[i]))
    with open(dir_path + "/"+file_name+".csv", "w") as csv_file:
        fieldnames = ["date", "number"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(per)):
            writer.writerow({"date":str(date[i]), "number":str(per[i])})