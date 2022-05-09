from os import write
import requests
import time
from datetime import datetime
import datetime
import pandas as pd
import json
from pandas.io.json import json_normalize
import csv
import sys
import re
import os
import glob
from tqdm import tqdm 


def input():
    repositories = sys.argv   ## owner/repositoryはrepository[1]以降に格納
    pattern = "(.*)/(.*)"
    d = re.search(pattern, repositories[1])
    owner = d.group(1)
    repository = d.group(2)
    dir_path = makedir(owner, repository)
    payload_1 = makepayload(owner, repository)
    return repository, dir_path, payload_1

def makedir(owner, repository):
    dir_path = "Extracted data/" + owner + "/"+ repository + "/" + "PullRequest"  ##現バージョンではstargazersだが後々属性値を指定できるようにする
    os.makedirs(dir_path, exist_ok=True)
    os.makedirs(os.path.join(dir_path, "CSV"), exist_ok=True)
    os.makedirs(os.path.join(dir_path, "json"), exist_ok=True)
    return dir_path

def makepayload(owner, repository):
    payload_1 = ("{\"query\":\"query PullRequests {\\n  repository(owner: \\\""+ owner + "\\\", name: \\\""+ repository + "\\\") {\\n    pullRequests(first: 100") 
    return payload_1


def request(repository, dir_path, payload_1, endCursor, hasNextPage,file_num): ##100件のスターを取得, 総ノード数は101.(1+100)
    print()
    sys.setrecursionlimit(10 ** 9)  ## 再帰回数の上限を変更 (10^9)
    data_cpl = False
    url = "https://api.github.com/graphql"
    payload_2 = ("){\\n        pageInfo{\\n        hasNextPage,\\n        endCursor\\n      }\\n      nodes{\\n        createdAt,\\n        additions,\\n        deletions,\\n      }\\n    }\\n  }\\n}\",\"operationName\":\"PullRequests\"}")
    if (hasNextPage == 1):
        if endCursor != None:
            payload = (payload_1 + ",after:"+"\\\""+ endCursor +"\\\""+ payload_2)
        else:
            payload = payload_1 + payload_2
            data_cpl = True
        headers = {
            "Authorization": "bearer  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",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        res = requests.get(url)
        #print("status code : "+str(res.status_code)) ##status code出力
        json_data = response.json()
        data = find(json_data, str(file_num), dir_path, data_cpl)
        file_nextnum = data[0]
        download_per(data[3], int(file_nextnum))
        export(file_nextnum, dir_path) #csvファイルに変換
        return request(repository, dir_path, payload_1, data[1],data[2],file_num)
    else: 
        return

    
def find(json_data, file_name, dir_path, data_cpl):
    list_of_files = glob.glob(os.path.join(dir_path, "json","*.json")) #list型 指定したフォルダからファイル一覧を取得

    if len(list_of_files) == 0 : ## 初回参照時 (フォルダにjsonファイルがない時)
        output(json_data, file_name, dir_path)
        print("初回作成時")
        f = open(os.path.join(dir_path, "json", file_name+".json"), "r")
        file_num = 2
        file_nextnum = 2

    else: ## 保存しているキャッシュディレクトリから，最新のファイルを参照する．
        file_intlist = []
        for file in list_of_files: # 絶対パスから拡張子を除いたファイル名のみを取得 
            filename,fileext = os.path.splitext(os.path.basename(file))
            file_intlist.append(filename)
        file_int = [int(s) for s in file_intlist]
        file_num = max(file_int)
        file_nextnum = str(max(file_int)+1)
        output(json_data, file_nextnum, dir_path)
        f = open(os.path.join(dir_path, "json", file_nextnum+".json"), "r")
    json_dict = json.load(f)
    endCursor = json_dict["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
    hasNextPage = json_dict["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
    return file_nextnum, endCursor, hasNextPage
    
    ##いずれ引数から属性値もファイル名にする.(今はstargazers)

def output(json_data,file_name,dir_path):
    with open(os.path.join(dir_path, "json",str(file_name)+".json"),"w") as f:
        #print(str(file_name)+".jsonを作成")
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def download_per(total, file_num):
    pbar = tqdm(total = total)
    pbar.update(file_num*100)

def export(file_name, dir_path):
    file_json= int(file_name) -1
    json_filename = str(file_json) + ".json"
    csv_filename = str(file_json) + ".csv"
    f = open(os.path.join(dir_path, "json", json_filename), "r")
    data = json.load(f)
    #print(csv_filename+"を作成")

    #
    # Set nodes Dictionary
    #
    nodes = []
    temp_n = []
    for node in data["data"]["repository"]["pullRequests"]["nodes"]:
        createdAt = node["createdAt"]
        additions = node["additions"]
        deletions = node["deletions"]
        created_utc = createdAt.replace('Z', '')
        d_c = datetime.datetime.fromisoformat(created_utc).date()
        createdt = str(d_c.year) + "-" + str(d_c.month)#+ "/" + str(d.day)
        temp_n = [createdt, additions, deletions]
        nodes.append(temp_n)

    #
    # Write CSV
    #
    with open(os.path.join(dir_path, "csv",csv_filename), 'w', newline = '') as csvFile:
        csvwriter = csv.writer(csvFile, delimiter=',',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writerow((['createdAt'], ['additions'], ["deletions"]))
        for value in nodes:
            csvwriter.writerow(value)


def merge(dir_path):
    # パスで指定したファイルの一覧をリスト形式で取得．
    path = os.path.join(dir_path, "CSV")
    csv_files = glob.glob(path + "/*.csv")
    data_list = []
    

    for i in range(1,len(csv_files)):
        if os.path.exists(path + "/" + str(i) + ".csv"):
            data_list.append(pd.read_csv(path + "/" + str(i) + ".csv"))
    
    df = pd.concat(data_list, axis=0, sort = True)

    df.to_csv(os.path.join(path, "total.csv"), index=False)
    


project = input()
list_of_files = glob.glob(os.path.join(project[1], "json","*.json")) #list型 指定したフォルダからファイル一覧を取得
if len(list_of_files) == 0 : ## 初回参照時 (フォルダにjsonファイルがない時)
    endCursor = None
    hasNextPage = True
    file_num = 1
    print("初回調査時")
else: ## 保存しているキャッシュディレクトリから，最新のファイルを参照する．
    file_list = max(list_of_files, key = os.path.getctime)
    file_num, fileext = os.path.splitext(os.path.basename(file_list)) #最新のファイルのNoのみ取得
    file_num = int(file_num)
    f = open(file_list, "r")
    
    json_dict = json.load(f)
    endCursor = json_dict["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
    hasNextPage = json_dict["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
request(project[0], project[1], project[2], endCursor, hasNextPage, file_num) ##stargazers取得

dir_path = project[1]
list_of_files = glob.glob(os.path.join(dir_path, "json","*.json")) #list型 指定したフォルダからファイル一覧を取得
file_intlist = []
for file in list_of_files: # 絶対パスから拡張子を除いたファイル名のみを取得 
    filename,fileext = os.path.splitext(os.path.basename(file))
    file_intlist.append(filename)
file_int = [int(s) for s in file_intlist]
file_num = max(file_int)
export(file_num+1, dir_path) #csvファイルに変換

merge(project[1])
print("データ取得完了")