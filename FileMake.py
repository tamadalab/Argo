import os
import re
import glob
import json
from pandas.io.json import json_normalize
import pandas as pd
import csv
import fig_process


def input(repository):
    pattern = "(.*)/(.*)"
    d = re.search(pattern, repository)
    owner = d.group(1)
    repository = d.group(2)
    return owner, repository


def makedir(owner, repository, metrics):
    dir_path = os.path.join("cache", owner, repository, metrics)
    os.makedirs(dir_path, exist_ok=True)
    os.makedirs(os.path.join(dir_path, "CSV"), exist_ok=True)
    os.makedirs(os.path.join(dir_path, "json"), exist_ok=True)
    return dir_path


def newmakedir(dir_path):
    os.makedirs(dir_path, exist_ok=True)
    os.makedirs(os.path.join(dir_path, "CSV"), exist_ok=True)
    os.makedirs(os.path.join(dir_path, "json"), exist_ok=True)
    return dir_path


def deletedir(dir_path):
    os.rmdir(dir_path)


def findCursor(dir_path, metrics):
    list_of_files = glob.glob(os.path.join(dir_path, "json", "*.json"))
    if len(list_of_files) == 0:
        endCursor = None
        hasNextPage = True
        file_num = 1
        print("First Survey")
    else:
        file_list = max(list_of_files, key=os.path.getctime)
        file_num, fileext = os.path.splitext(os.path.basename(file_list))
        file_num = int(file_num)
        with open(file_list, "r") as f:
            json_dict = json.load(f)
        if metrics == "stargazers":
            json_data = Star(json_dict)
        elif metrics == "pullRequests":
            json_data = Pullrequests(json_dict)
        elif metrics == "issues":
            json_data = Issue(json_dict)
        endCursor = json_data[0]
        hasNextPage = json_data[1]
    return endCursor, hasNextPage, file_num


def Star(json_dict):
    endCursor = json_dict["data"]["repository"]["stargazers"]["pageInfo"]["endCursor"]
    hasNextPage = json_dict["data"]["repository"]["stargazers"]["pageInfo"]["hasNextPage"]
    return endCursor, hasNextPage


def Pullrequests(json_dict):
    endCursor = json_dict["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
    hasNextPage = json_dict["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
    return endCursor, hasNextPage


def Issue(json_dict):
    endCursor = json_dict["data"]["repository"]["issues"]["pageInfo"]["endCursor"]
    hasNextPage = json_dict["data"]["repository"]["issues"]["pageInfo"]["hasNextPage"]
    return endCursor, hasNextPage


def jsonMake(json_data, file_name, dir_path):
    with open(os.path.join(dir_path, "json", str(file_name) + ".json"), "w") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def csvPrep(dir_path):
    list_of_files = glob.glob(os.path.join(dir_path, "json", "*.json"))
    file_intlist = []
    for file in list_of_files:
        filename, fileext = os.path.splitext(os.path.basename(file))
        file_intlist.append(filename)
    file_int = [int(s) for s in file_intlist]
    file_num = max(file_int)
    return file_num


def merge(dir_path):
    path = os.path.join(dir_path, "CSV")
    csv_files = glob.glob(path + "/*.csv")
    data_list = []

    for i in range(1, len(csv_files) + 1):
        if os.path.exists(os.path.join(path, str(i) + ".csv")):
            data_list.append(pd.read_csv(os.path.join(path, str(i) + ".csv")))
    df = pd.concat(data_list, axis=0, sort=True)
    df.to_csv(os.path.join(path, "total.csv"), index=False)


def output_data(repository, metrics, plotdata):
    dir_path = os.path.join("cache", repository, metrics)
    fig_process.makedir(dir_path)
    file = os.path.join(dir_path, "plot_data.csv")
    with open(file, "a") as f:
        writer = csv.writer(f)
        writer.writerow(plotdata)
