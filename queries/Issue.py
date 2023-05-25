import requests
import datetime
import pandas as pd
import json
import csv
import sys
import os
import glob
import FileMake
import Download_per
from tqdm import tqdm
import time

# Issue取得Payloadの作成
def make_payload(owner, repository):
    payload_1 = (
        "{\"query\":\"query issues {\\n  repository(owner: \\\""
        + owner
        + "\\\", name: \\\""
        + repository
        + "\\\") {\\n    issues(first: 100"
    )
    return payload_1

# GitHub GraphQL APIへデータリクエスト
def request(repository, dir_path, payload_1, end_cursor, has_next_page, file_num):
    print()
    sys.setrecursionlimit(10 ** 9) ## 再帰回数の上限を変更 (10^9)
    data_complete = False
    url = "https://api.github.com/graphql"
    payload_2 = "){\\n      totalCount\\n      nodes{\\n        title\\n        url\\n      createdAt\\n        closedAt\\n            }\\n      pageInfo{\\n        endCursor\\n        hasNextPage\\n      }\\n    }\\n  }\\n}\\n\",\"operationName\":\"issues\"}"
    
    if has_next_page == 1:
        if end_cursor != None:
            payload = payload_1 + ",after:" + "\\\"" + end_cursor + "\\\"" + payload_2
        else:
            payload = payload_1 + payload_2
            data_complete = True
        headers = {
            "Authorization": "bearer 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",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        res = requests.get(url)
        json_data = response.json()
        data = find(json_data, str(file_num), dir_path, data_complete)
        file_next_num = data[0]
        Download_per.download_per(data[3], int(file_next_num))
        export(file_next_num, dir_path) # csvファイルに変換
        return request(repository, dir_path, payload_1, data[1], data[2], file_num)
    else:
        return

# 既存ファイルの有無の確認
def find(json_data, file_name, dir_path, data_complete):
    list_of_files = glob.glob(os.path.join(dir_path, "json", "*.json")) # list型 指定したフォルダからファイル一覧を取得

    if len(list_of_files) == 0: ## 初回参照時 (フォルダにjsonファイルがない時)
        FileMake.json_make(json_data, file_name, dir_path)
        print("Initial data retrieval")
        f = open(os.path.join(dir_path, "json", file_name + ".json"), "r")
        file_next_num = 2
    else: ## 保存しているキャッシュディレクトリから，最新のファイルを参照する．
        file_int_list = []
        for file in list_of_files: # 絶対パスから拡張子を除いたファイル名のみを取得
            filename, file_ext = os.path.splitext(os.path.basename(file))
            file_int_list.append(filename)
        file_int = [int(s) for s in file_int_list]
        file_num = max(file_int)
        file_next_num = str(max(file_int) + 1)
        FileMake.json_make(json_data, file_next_num, dir_path)
        f = open(os.path.join(dir_path, "json", file_next_num + ".json"), "r")
    json_dict = json.load(f)
    total_count = json_dict["data"]["repository"]["issues"]["totalCount"]
    end_cursor = json_dict["data"]["repository"]["issues"]["pageInfo"]["endCursor"]
    has_next_page = json_dict["data"]["repository"]["issues"]["pageInfo"]["hasNextPage"]
    return file_next_num, end_cursor, has_next_page, total_count

# csvファイル変換
def export(file_name, dir_path):
    file_json = int(file_name) - 1
    json_filename = str(file_json) + ".json"
    csv_filename = str(file_json) + ".csv"
    f = open(os.path.join(dir_path, "json", json_filename), "r")
    data = json.load(f)
    
    # Set nodes Dictionary
    nodes = []
    temp_n = []
    for node in data["data"]["repository"]["issues"]["nodes"]:
        title = node["title"]
        url = node["url"]
        created_at = node["createdAt"]
        closed_at = node["closedAt"]

        created_utc = created_at.replace("Z", "")
        d = datetime.datetime.fromisoformat(created_utc).date()
        createdt = f"{d.year}-{d.month}/{d.day}"
        
        if not closed_at:
            closedt = "null"
        else:
            closedt_utc = closed_at.replace("Z", "")
            d = datetime.datetime.fromisoformat(closedt_utc).date()
            closedt = f"{d.year}-{d.month}/{d.day}"

        temp_n = [title, url, createdt, closedt]
        nodes.append(temp_n)
    
    # Write CSV
    with open(
        os.path.join(dir_path, "csv", csv_filename), "w", newline=""
    ) as csv_file:
        csv_writer = csv.writer(
            csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC
        )
        csv_writer.writerow(
            [
                ["title"], 
                ["url"], 
                ["createdAt"], 
                ["closedAt"]
            ]
        )
        for value in nodes:
            csv_writer.writerow(value)


def main(repository, make_path, dir_stored):
    start_time = time.perf_counter()

    for i in range(len(repository)):
        # Make File, Payload
        repo_data = FileMake.input(repository[i])
        print(make_path)
        if make_path == True:
            dir_path = FileMake.makedir(repo_data[0], repo_data[1], "issues")
        else:
            dir_path = FileMake.newmakedir(make_path)
        payload = make_payload(repo_data[0], repo_data[1])

        # Get json_data
        json_data = FileMake.find_cursor(dir_path, "issues")
        request(
            repo_data[1], dir_path, payload, json_data[0], json_data[1], json_data[2]
        )

        # Export csv_data
        file_num = FileMake.csv_prep(dir_path)
        export(file_num + 1, dir_path) # csvファイルに変換
        FileMake.merge(dir_path)
        
        # Delete cache
        if dir_stored == True:
            FileMake.delete_dir(dir_path)

    end_time = time.perf_counter()
    print("Data acquisition completed! : " + str(end_time - start_time) + "s")


if __name__ == "__main__":
    repositories = sys.argv[1:]
    dir_path = True
    dir_stored = False

    main(repositories, dir_path, dir_stored)
