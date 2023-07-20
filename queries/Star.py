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
        "{\"query\":\"query stargazers {\\n  repository(owner: \\\""
        + owner
        + "\\\", name: \\\""
        + repository
        + "\\\") {\\n    stargazers(first: 100"
    )
    return payload_1


# Request data from GitHub GraphQL API
def request(repository, dir_path, payload_1, end_cursor, has_next_page, file_num):
    print()
    sys.setrecursionlimit(10 ** 9)  ## Change recursion limit (10^9)
    data_cpl = False
    url = "https://api.github.com/graphql"
    payload_2 = (
        "){\\n      totalCount\\n      nodes{\\n        name\\n        login\\n      }\\n      edges{\\n        cursor\\n        starredAt\\n      }\\n      pageInfo{\\n        endCursor\\n        hasNextPage\\n      }\\n    }\\n  }\\n}\\n\",\"operationName\":\"stargazers\"}"
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
        headers = {
            "Authorization": "bearer  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",
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
    totalCount = json_dict["data"]["repository"]["stargazers"]["totalCount"]
    end_cursor = json_dict["data"]["repository"]["stargazers"]["pageInfo"]["endCursor"]
    has_next_page = json_dict["data"]["repository"]["stargazers"]["pageInfo"]["hasNextPage"]
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
    for node in data["data"]["repository"]["stargazers"]["nodes"]:
        login = node["login"]
        nodes.append([login])

    # Set edges Dictionary
    edges = []
    temp_e = []
    date = []
    for edge in data["data"]["repository"]["stargazers"]["edges"]:
        cursor = edge["cursor"]
        starredAt = edge["starredAt"]
        dt_utc = starredAt.replace("Z", "")
        d = datetime.datetime.fromisoformat(dt_utc).date()
        date = str(d.year) + "-" + str(d.month)
        temp_e = [cursor, date]
        edges.append(temp_e)

    # Get value
    values = nodes
    for i in range(len(nodes)):
        values[i].extend(edges[i])  # Combine matrices

    # Write CSV
    with open(os.path.join(dir_path, "csv", csv_filename), "w", newline="") as csvFile:
        csvwriter = csv.writer(
            csvFile, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC
        )
        csvwriter.writerow(["login", "cursor", "starredAt"])
        csvwriter.writerows(values)


def main(repository, make_path, dir_stored):
    start_time = time.perf_counter()

    for i in range(len(repository)):
        # Make File, Payload
        print("Download repository: " + repository[i])
        repo_data = FileMake.input(repository[i])  # owner, repository
        if make_path:
            dir_path = FileMake.makedir(repo_data[0], repo_data[1], "Star")
        else:
            dir_path = FileMake.newmakedir(make_path)
        payload = make_payload(repo_data[0], repo_data[1])

        # Get json_data
        json_data = FileMake.findCursor(dir_path, "stargazers")  # endCursor, hasNextPage, file_num
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
