import os
import sys
import csv
import re
import datetime
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

import fig_process
import FileMake


def prep(file):
    csv_input = pd.read_csv(file, encoding="UTF-8", sep=",")
    create_list = []
    close_list = []
    date_list = []
    dt_now = datetime.datetime.now()
    dt_YearMonth = f"{dt_now.year}-{dt_now.month}/{dt_now.day}"

    for i in range(len(csv_input.index)):
        create = csv_input.iat[i, 1]
        create_list.append(create)
        if isinstance(csv_input.iat[i, 0], float):
            close = dt_YearMonth
        else:
            close = csv_input.iat[i, 0]
        close_list.append(close)
        date_list.append([create, close])

    date_list = sorted(date_list, key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m/%d'))
    create_list = sorted(create_list, key=lambda x: datetime.datetime.strptime(x, '%Y-%m/%d'))

    c = Counter(create_list)
    keys = []
    diff_date = diff(dt_YearMonth, create_list[0])
    diff = 12 * diff_date[0] + diff_date[1]
    year = create_list[0][:4]
    create = re.findall(r"\d+", create_list[0])

    for i in range(diff + 1):
        if i == 0:
            keys.append(f"{create[0]}-{create[1]}")
            month = int(re.findall('-(.*)/', create_list[0])[0])
        else:
            keys.append(f"{year}-{month}")

        if month == 12:
            year = int(year) + 1
            month = 1
        else:
            month = int(month) + 1

    scale = [0]
    year = [int(keys[0][:4])]
    for i in range(1, len(keys)):
        if keys[i].endswith("-1"):
            scale.append(i)
            if keys[i][:4] not in year:
                year.append(int(keys[i][:4]))

    createdAt = list(c.keys())
    createdAt = list(set([re.findall(r"\d+", key)[0] + "-" + re.findall(r"\d+", key)[1] for key in createdAt]))

    livetime_list = livetime(date_list)
    return createdAt, livetime_list, scale, year


def livetime(date_list):
    livetime_list = []
    for i in range(len(date_list)):
        diff_date = diff(date_list[i][1], date_list[i][0])
        create_date = re.findall(r"\d+", date_list[i][0])
        livetime = (diff_date[0] * 365) + (diff_date[1] * 31) + diff_date[2]
        if i == 0:
            std_month = 0
            num_month = 0
            livetime_total = livetime
        elif i == len(date_list) - 1:
            try:
                num_date = livetime_total / num_month
            except ZeroDivisionError:
                num_date = livetime_total
            livetime_list.append(num_date)
        else:
            if re.findall('-(.*)/', date_list[i][0])[0] == re.findall('-(.*)/', date_list[i - 1][0])[0]:
                livetime_total += livetime
                num_month += 1
            else:
                livetime_total = livetime
                std_month += 1
                try:
                    num_date = livetime_total / num_month
                except ZeroDivisionError:
                    num_date = livetime_total
                livetime_list.append(num_date)
                num_month = 0
    return livetime_list


def xticks(dt_now, first_create):
    diff_date = diff(dt_now, first_create)
    diff = 12 * diff_date[0] + diff_date[1]
    values = [0] * (diff + 1)
    return values


def diff(now_create, first_create):
    create = re.findall(r"\d+", first_create)
    close = re.findall(r"\d+", now_create)
    year = int(close[0]) - int(create[0])
    month = int(close[1]) - int(create[1])
    day = int(close[2]) - int(create[2])
    return year, month, day


def com_plot(file, keys, values):
    plt.plot(keys, values, label=file, marker=".")
    plt.legend()
    plt.title("LT_CIS")
    plt.xlabel("date")
    plt.ylabel("Live_time(day)")
    plt.grid(alpha=0.6)


def scale(year, years):
    for i in range(len(year)):
        if not years:
            years.append(year[i])
        elif year[i] not in years:
            years.append(year[i])
    years = sorted(years)
    return years


def main(arg, format, dir_path, write_data):
    plt.rcParams["figure.figsize"] = (8, 6)
    figure = plt.figure()

    years = []
    files = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "issues/CSV/total.csv")
        dict = prep(file)
        years = scale(dict[3], years)
        year = dict[3]
        if year[0] == years[0]:
            files.insert(0, file)
        else:
            files.append(file)

    for i in range(len(files)):
        dict = prep(files[i])
        label = re.findall("e/(.*)/i", str(files[i]))[0].strip("[""]")
        if write_data is not None:
            fig_process.Print(label, dict[0], dict[1])
        com_plot(label, dict[0], dict[1])
        if i == 0:
            plt.xticks(dict[2], dict[3])

    fig_process.makedir(dir_path)
    for i in range(len(files)):
        fig_process.savefig(figure, f"{dir_path}/LT_CIS", format)
        fig_process.makedir(f"cache/{arg[i]}/LT_CIS")
        file = os.path.join("cache", arg[i], "LT_CIS/plot_data.csv")
        with open(file, "w") as f:
            writer = csv.writer(f)
            writer.writerow(dict[0])
            writer.writerow(dict[1])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    arg = sys.argv[1:]
    format = 'svg'
    dir_path = 'Graph_image'
    write_data = None
    main(arg, format, dir_path, write_data)
