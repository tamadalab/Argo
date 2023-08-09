import os
import re
import glob
import json
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
    dir_path = "cache/" + owner + "/"+ repository + "/" + metrics 
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
    list_of_files = glob.glob(os.path.join(dir_path, "json","*.json")) #list型 指定したフォルダからファイル一覧を取得
    if len(list_of_files) == 0 : ## 初回参照時 (フォルダにjsonファイルがない時)
        endCursor = None
        hasNextPage = True
        file_num = 1
        print("First Survey")
    else: ## 保存しているキャッシュディレクトリから，最新のファイルを参照する．
        file_list = max(list_of_files, key = os.path.getctime)
        file_num, fileext = os.path.splitext(os.path.basename(file_list)) #最新のファイルのNoのみ取得
        file_num = int(file_num)
        f = open(file_list, "r")
        json_dict = json.load(f)
        if metrics == "stargazers":
            json_data = Star(json_dict)
        elif metrics == "pullRequests":
            json_data = Pullrequests(json_dict)
        elif metrics == "issues":
            json_data = Issue(json_dict)
        elif metrics == "commits":
            json_data = Commit(json_dict)
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

def Commit(json_dict):
        endCursor = json_dict["data"]["repository"]["defaultBranchRef"]["target"]["history"]["pageInfo"]["endCursor"]
        hasNextPage = json_dict["data"]["repository"]["defaultBranchRef"]["target"]["history"]["pageInfo"]["hasNextPage"]
        return endCursor, hasNextPage

def jsonMake(json_data,file_name,dir_path):
    with open(os.path.join(dir_path, "json",str(file_name)+".json"),"w") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def csvPrep(dir_path):
    list_of_files = glob.glob(os.path.join(dir_path, "json","*.json")) #list型 指定したフォルダからファイル一覧を取得
    file_intlist = []
    for file in list_of_files: # 絶対パスから拡張子を除いたファイル名のみを取得 
        filename,fileext = os.path.splitext(os.path.basename(file))
        file_intlist.append(filename)
    file_int = [int(s) for s in file_intlist]
    file_num = max(file_int)
    return file_num

def merge(dir_path):
    # パスで指定したファイルの一覧をリスト形式で取得する．
    path = os.path.join(dir_path, "CSV")
    csv_files = glob.glob(path + "/*.csv")
    data_list = []

    # 全てのcsvファイルを読み込み，total.csvファイルを作成する．
    for i in range(1,len(csv_files)+1):
        # total.csvファイルが存在しないとき，作成する．
        if os.path.exists(path + "/" + str(i) + ".csv"):
            data_list.append(pd.read_csv(path + "/" + str(i) + ".csv"))
    df = pd.concat(data_list, axis=0, sort = False)
    with open(os.path.join(path, "total.csv"), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(df.columns)  # 列のヘッダーを書き込む
        for row in df.values:
            writer.writerow(row)

def output_data(repository,metrics, plotdata):
    fig_process.makedir("cache/" + repository +"/"+ metrics)
    file = os.path.join("cache", repository, metrics, "/plot_data.csv")
    with open(file, "a") as f:
        writer = csv.writer(f)
        writer.writerow(plotdata)

def reverse_csv_rows(csv_file):
    with open(csv_file, 'r') as f:
        rows = list(csv.reader(f))

    reversed_rows = list(zip(*rows[::-1]))

    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(reversed_rows)

def sort_csvfile(csv_file):

    # データを読み込む
    data = pd.read_csv(csv_file)

    # createdAt列を年月のデータとして解釈し、ソートする
    data['createdAt'] = pd.to_datetime(data['createdAt'], format='%Y-%m/%d')
    data_sorted = data.sort_values('createdAt')

    # createdAt列の形式を元に戻す
    data_sorted['createdAt'] = data_sorted['createdAt'].dt.strftime('%Y-%m/%d')

    # ソート結果を元のCSVファイルに上書きする
    data_sorted.to_csv(csv_file, index=False)