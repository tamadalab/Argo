from os import write
import requests
from datetime import datetime
import datetime
import pandas as pd
import json
from pandas.io.json import json_normalize
import csv
import sys
import os
import glob
import FileMake
import Download_per
from tqdm import tqdm
import time


def makepayload(owner, repository):
    payload_1 = ("{\"query\":\"query issues {\\n  repository(owner: \\\""+ owner + "\\\", name: \\\""+ repository + "\\\") {\\n    issues(first: 100") 
    return payload_1


def request(repository, dir_path, payload_1, endCursor, hasNextPage,file_num): ##100件のスターを取得, 総ノード数は101.(1+100)
    print()
    sys.setrecursionlimit(10 ** 9)  ## 再帰回数の上限を変更 (10^9)
    data_cpl = False
    url = "https://api.github.com/graphql"
    payload_2 = ("){\\n      totalCount\\n      nodes{\\n        title\\n        url\\n      createdAt\\n        closedAt\\n            }\\n      pageInfo{\\n        endCursor\\n        hasNextPage\\n      }\\n    }\\n  }\\n}\\n\",\"operationName\":\"issues\"}")
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
        Download_per.download_per(data[3], int(file_nextnum))
        export(file_nextnum, dir_path) #csvファイルに変換
        return request(repository, dir_path, payload_1, data[1],data[2],file_num)
    else: 
        return

    
def find(json_data, file_name, dir_path, data_cpl):
    list_of_files = glob.glob(os.path.join(dir_path, "json","*.json")) #list型 指定したフォルダからファイル一覧を取得

    if len(list_of_files) == 0 : ## 初回参照時 (フォルダにjsonファイルがない時)
        FileMake.jsonMake(json_data, file_name, dir_path)
        print("初回データ取得")
        f = open(os.path.join(dir_path, "json", file_name+".json"), "r")
        file_nextnum = 2

    else: ## 保存しているキャッシュディレクトリから，最新のファイルを参照する．
        file_intlist = []
        for file in list_of_files: # 絶対パスから拡張子を除いたファイル名のみを取得 
            filename,fileext = os.path.splitext(os.path.basename(file))
            file_intlist.append(filename)
        file_int = [int(s) for s in file_intlist]
        file_num = max(file_int)
        file_nextnum = str(max(file_int)+1)
        FileMake.jsonMake(json_data, file_nextnum, dir_path)
        f = open(os.path.join(dir_path, "json", file_nextnum+".json"), "r")
    json_dict = json.load(f)
    totalCount = json_dict["data"]["repository"]["issues"]["totalCount"]
    endCursor = json_dict["data"]["repository"]["issues"]["pageInfo"]["endCursor"]
    hasNextPage = json_dict["data"]["repository"]["issues"]["pageInfo"]["hasNextPage"]
    return file_nextnum, endCursor, hasNextPage, totalCount
    
    ##いずれ引数から属性値もファイル名にする.(今はstargazers)

def export(file_name, dir_path):
    file_json= int(file_name) -1
    json_filename = str(file_json) + ".json"
    csv_filename = str(file_json) + ".csv"
    f = open(os.path.join(dir_path, "json", json_filename), "r")
    data = json.load(f)

    #
    # Set nodes Dictionary
    #
    nodes = []
    temp_n = []
    for node in data["data"]["repository"]["issues"]["nodes"]:
        title = node["title"]
        url = node["url"]
        createdAt = node["createdAt"]
        closedAt = node["closedAt"]
        
        created_utc = createdAt.replace('Z', '')
        d = datetime.datetime.fromisoformat(created_utc).date()
        createdt = str(d.year) + "-" + str(d.month)+ "/" + str(d.day)
        if not closedAt: # closeされていないとき
            closedt = "null"
        else:    
            closedt_utc = closedAt.replace('Z', '')
            d = datetime.datetime.fromisoformat(closedt_utc).date()
            closedt = str(d.year) + "-" + str(d.month) + "/" + str(d.day)

        temp_n = [title, url, createdt, closedt]
        nodes.append(temp_n)
    
    #
    # Write CSV
    #
    with open(os.path.join(dir_path, "csv",csv_filename), 'w', newline = '') as csvFile:
        csvwriter = csv.writer(csvFile, delimiter=',',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writerow((['title'], ['url'], ['createdAt'],['closedAt']))
        for value in nodes:
            csvwriter.writerow(value)

def main(repository, make_path, dir_stored): 
    start_time = time.perf_counter()
    
    for i in range(len(repository)):
        # Make File, Payload
        repo_data = FileMake.input(repository[i]) ## owner, repository
        print(make_path)
        if make_path == True:
            dir_path = FileMake.makedir(repo_data[0],repo_data[1],"issues")
        else:
            dir_path = FileMake.newmakedir(make_path)
        payload = makepayload(repo_data[0], repo_data[1])
        
        # Get json_data
        json_data = FileMake.findCursor(dir_path, "issues") #endCursor, hasNextPage, file_num
        request(repo_data[1], dir_path, payload, json_data[0], json_data[1], json_data[2]) ##stargazers取得
        
        # Export csv_data
        file_num = FileMake.csvPrep(dir_path)
        export(file_num+1, dir_path) #csvファイルに変換
        FileMake.merge(dir_path)
        
        # Delete cache
        if dir_stored == True:
            FileMake.deletedir(dir_path)
    
    
    end_time = time.perf_counter()
    print("Data acquisition completed! : " + str(end_time - start_time) + "s")

if __name__ == "__main__":
    repositories = sys.argv   ## owner/repositoryはrepository[1]以降に格納
    repositories.pop(0) ##repositorirs[0](~.py)を削除
    dir_path = True
    dir_stored = False
    
    main(repositories, dir_path, dir_stored)