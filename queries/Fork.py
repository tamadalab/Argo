import requests
from datetime import datetime
import datetime
import csv
import sys
import os
import glob
import time
import json

import FileMake
import Download_per


# Create payload for retrieving Star data
def make_payload(owner, repository):
    payload_1 = (
        "{\"query\":\"query forks {\\n  repository(owner: \\\""
        + owner
        + "\\\", name: \\\""
        + repository
        + "\\\") {\\n    forks(first: 100"
    )
    return payload_1


# Request data from GitHub GraphQL API
def request(repository, dir_path, payload_1, end_cursor, has_next_page, file_num):
    print()
    sys.setrecursionlimit(10 ** 9)  ## Change recursion limit (10^9)
    data_cpl = False
    url = "https://api.github.com/graphql"
    payload_2 = (
        ") {\\n\\t\\t\\ttotalCount\\n\\t\\t\\tnodes {\\n\\t\\t\\t\\tnameWithOwner\\n\\t\\t\\t\\turl\\n\\t\\t\\t\\tcreatedAt\\n\\t\\t\\t\\tdefaultBranchRef {\\n\\t\\t\\t\\t\\ttarget {\\n\\t\\t\\t\\t\\t\\t... on Commit {\\n\\t\\t\\t\\t\\t\\t\\tcommittedDate\\n\\t\\t\\t\\t\\t\\t}\\n\\t\\t\\t\\t\\t}\\n\\t\\t\\t\\t}\\n\\t\\t\\t}\\n\\t\\t\\tpageInfo{\\n\\t\\t\\t\\tendCursor\\n\\t\\t\\t\\thasNextPage\\n\\t\\t\\t}\\n\\t\\t}\\n\\t}\\n}\",\"operationName\":\"forks\"}"
    )
    if has_next_page == 1:
        if end_cursor != None:
            payload = (
                payload_1
                + ",after:"
                + "\\\""
                + end_cursor
                + "\\\""
                + payload_2
            )
        else:
            payload = payload_1 + payload_2
            data_cpl = True
        
        api_key = os.getenv('GITHUB_API_KEY')
        if api_key is None:
            raise Exception("Couldn't find the GitHub API key. Please set it as an environment variable.")

        headers = {
            "Authorization": "bearer " + api_key,
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        res = requests.get(url)
        # print("status code : "+str(res.status_code)) ## Output status code
        json_data = response.json()
        data = find(json_data, str(file_num), dir_path, data_cpl)
        file_nextnum = data[0]
        Download_per.download_per(data[3], int(file_nextnum))
        export(file_nextnum, dir_path)  # Convert to CSV file
        return request(repository, dir_path, payload_1, data[1], data[2], file_num)
    else:
        return


# Check if existing files exist
def find(json_data, file_name, dir_path, data_cpl):
    list_of_files = glob.glob(os.path.join(dir_path, "json", "*.json"))  # Get the list of files from the specified folder

    if len(list_of_files) == 0:  # When referring for the first time (no json files in the folder)
        FileMake.jsonMake(json_data, file_name, dir_path)
        print("First Survey")
        f = open(os.path.join(dir_path, "json", file_name + ".json"), "r")
        file_nextnum = 2

    else:  # Refer to the latest file from the cached directory
        file_intlist = []
        for file in list_of_files:  # Get only the file name without the extension from the absolute path
            filename, fileext = os.path.splitext(os.path.basename(file))
            file_intlist.append(filename)
        file_int = [int(s) for s in file_intlist]
        file_nextnum = str(max(file_int) + 1)
        FileMake.jsonMake(json_data, file_nextnum, dir_path)
        f = open(os.path.join(dir_path, "json", file_nextnum + ".json"), "r")
    json_dict = json.load(f)
    
    json_file_path = os.path.join(dir_path, "json",str(file_name)+".json")
    retry_limit = 5
    retry_count = 0

    while retry_count < retry_limit:
        try:
            # エラーが起きうる可能性のあるコード
            totalCount = json_dict["data"]["repository"]["forks"]["totalCount"]
            break
        except TypeError:
            if os.path.isfile(json_file_path):
                os.remove(json_file_path)
            retry_count += 1
            print(f"Error occurred, retrying... ({retry_count}/{retry_limit})")
            # 待機時間を設ける
            time.sleep(1)  # 1秒待機
    else:
        print(f"Error occurred {retry_limit} times. Stop retrying.")

    end_cursor = json_dict["data"]["repository"]["forks"]["pageInfo"]["endCursor"]
    has_next_page = json_dict["data"]["repository"]["forks"]["pageInfo"]["hasNextPage"]
    return file_nextnum, end_cursor, has_next_page, totalCount


# Convert to CSV file
def export(file_name, dir_path):
    file_json = int(file_name) - 1
    json_filename = str(file_json) + ".json"
    csv_filename = str(file_json) + ".csv"
    f = open(os.path.join(dir_path, "json", json_filename), "r")
    data = json.load(f)

    # Set nodes Dictionary
    nodes = []
    temp_n = []
    for node in data["data"]["repository"]["forks"]["nodes"]:
        nameWithOwner = node["nameWithOwner"]
        url = node["url"]
        createdAt = node["createdAt"]
            
        json_file_path = os.path.join(dir_path, "json",str(file_name)+".json")
        retry_limit = 5
        retry_count = 0

        while retry_count < retry_limit:
            try:
                # エラーが起きうる可能性のあるコード
                committedDate = node["defaultBranchRef"]["target"]["committedDate"]
                break
            except TypeError:
                if os.path.isfile(json_file_path):
                    os.remove(json_file_path)
                retry_count += 1
                print(f"Error occurred, retrying... ({retry_count}/{retry_limit})")
                # 待機時間を設ける
                time.sleep(1)  # 1秒待機
        else:
            print(f"Error occurred {retry_limit} times. Stop retrying.")
        
        created_utc = createdAt.replace("Z", "")
        d = datetime.datetime.fromisoformat(created_utc)
        createdt = d.strftime("%Y-%m/%d %H:%M:%S")

        committed_utc = committedDate.replace("Z", "")
        d = datetime.datetime.fromisoformat(committed_utc)
        committedt = d.strftime("%Y-%m/%d %H:%M:%S")

        temp_n = [nameWithOwner, url, createdt, committedt]
        nodes.append(temp_n)

    # Write CSV
    with open(os.path.join(dir_path, "csv", csv_filename), "w", newline="") as csvFile:
        csvwriter = csv.writer(
            csvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC
        )
        csvwriter.writerow(["nameWithOwner", "url", "createdAt", "committedDate"])
        for value in nodes:
            csvwriter.writerow(value)


def main(repository, make_path, dir_stored):
    start_time = time.perf_counter()

    for i in range(len(repository)):
        # Make File, Payload
        print("Download repository: " + repository[i])
        repo_data = FileMake.input(repository[i])  # owner, repository
        if make_path:
            dir_path = FileMake.makedir(repo_data[0], repo_data[1], "Fork")
        else:
            dir_path = FileMake.newmakedir(make_path)
        payload = make_payload(repo_data[0], repo_data[1])

        # Get json_data
        json_data = FileMake.findCursor(dir_path, "forks")  # endCursor, hasNextPage, file_num
        request(
            repo_data[1], dir_path, payload, json_data[0], json_data[1], json_data[2]
        )  # Retrieve stargazers

        # Export csv_data
        file_num = FileMake.csvPrep(dir_path)
        export(file_num + 1, dir_path)  # Convert to CSV file
        FileMake.merge(dir_path)

        # Delete cache
        if dir_stored:
            FileMake.deletedir(dir_path)

    end_time = time.perf_counter()
    print("Data acquisition completed! Duration: " + str(end_time - start_time) + "s")


if __name__ == "__main__":
    repositories = sys.argv  # owner/repository are stored from repository[1] onwards
    repositories.pop(0)  # Remove repositories[0] (~.py)
    dir_path = True
    dir_stored = False
    main(repositories, dir_path, dir_stored)
