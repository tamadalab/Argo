import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
import os
import re
import collections
import csv
import itertools

import fig_process


# データの前処理
def prep(file):
    csv_input = pd.read_csv(file, encoding="UTF-8", sep=",")

    create_list = []
    close_list = []
    dt_now = datetime.datetime.now()
    now_date = []
    dt_YearMonth = f"{dt_now.year}-{dt_now.month}"
    now_date.append(dt_YearMonth)

    for i in range(len(csv_input.index)):
        create_list.append(re.findall("(.*)/", csv_input.iat[i, 1]))
        if isinstance(csv_input.iat[i, 0], float):
            close_list.append(now_date)
        else:
            close_month = re.findall("(.*)/", csv_input.iat[i, 0])
            close_list.append(close_month)

    create_list = list(itertools.chain.from_iterable(create_list))
    close_list = list(itertools.chain.from_iterable(close_list))
    c = collections.Counter(create_list)

    diff = diff(dt_YearMonth, create_list[0])

    year = []
    scale = []
    i = 0
    for key in c.keys():
        if not year:
            year.append(key[:4])
            scale.append(i)
        elif key[:4] not in year:
            year.append(key[:4])
            scale.append(i)
        i += 1

    c = collections.Counter(create_list)
    test = [key for key, value in zip(c.keys(), c.values())]

    accum = []
    for value in c.values():
        if len(accum) == 0:
            accum.append(int(value))
        else:
            total = int(value) + accum[len(accum) - 1]
            accum.append(total)

    remIssue_prd = []
    target = "-"
    for i in range(len(create_list)):
        diff = diff(close_list[i], create_list[i])
        remIssue_prd.append(diff)

    values = x_ticks(dt_now, create_list[0])

    for i in range(len(create_list)):
        start_num = diff(create_list[i], create_list[0])
        for n in range(remIssue_prd[i] + 1):
            values[start_num] += 1
            start_num += 1

    r_ris = []
    for accum, value in zip(accum, values):
        per = (value / accum) * 100
        if per > 100:
            per = 100
        r_ris.append(per)

    return test, values, scale, year, r_ris, test


def x_ticks(dt_now, first_create):
    target = "-"
    Year = dt_now.year - int(first_create[:4])
    idx_create = first_create.find(target)
    create_month = first_create[idx_create + 1:]
    Month = dt_now.month - int(create_month)
    diff = 12 * Year + Month

    values = [0] * (diff + 1)
    return values


def diff(now_create, first_create):
    target = "-"
    Year = int(now_create[:4]) - int(first_create[:4])
    idx_now = now_create.find(target)
    now = now_create[idx_now + 1:]
    idx_first = first_create.find(target)
    first = first_create[idx_first + 1:]
    Month = int(now) - int(first)
    diff = 12 * Year + Month
    return diff


def com_plot(file, keys, r_ris):
    plt.plot(keys, r_ris, label=file, marker=".")
    plt.legend()
    plt.title("R-RIS")
    plt.xlabel("date")
    plt.ylabel("percent")
    plt.grid(alpha=0.6)


def scale(year, years):
    for i in range(len(year)):
        if not years:
            years.append(year[i])
        elif year[i] not in years:
            years.append(year[i])
    years = sorted(years)
    return years


def print_data(file, per, date):
    print(file)
    for i in range(len(per)):
        print(f"{date[i]}: {per[i]}")


def main(arg, file_format, dir_path, write_data):
    plt.rcParams["figure.figsize"] = (8, 6)
    figure = plt.figure()

    years = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "issues/CSV/total.csv")
        data_dict = prep(file)
        years = scale(data_dict[3], years)

    files = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "issues/CSV/total.csv")
        data_dict = prep(file)
        year = data_dict[3]
        if year[0] == years[0]:
            files.insert(0, file)
        else:
            files.append(file)

    for i in range(len(files)):
        data_dict = prep(files[i])
        label = re.findall("e/(.*)/i", str(files[i]))
        label = label[0].strip("[""]")
        if write_data is not None:
            print_data(label, data_dict[4], data_dict[5], write_data)
        com_plot(label, data_dict[0], data_dict[4])
        print_data(label, data_dict[4], data_dict[5])
        if i == 0:
            plt.xticks(data_dict[2], data_dict[3])

    fig_process.make_dir(dir_path)
    for i in range(len(files)):
        fig_process.savefig(figure, dir_path + '/' + "R_RIS", file_format)
        fig_process.make_dir(f"cache/{arg[i]}/R_RIS")
        file = os.path.join("cache", arg[i], "R_RIS/plot_data.csv")
        with open(file, "w") as f:
            writer = csv.writer(f)
            writer.writerow(data_dict[0])
            writer.writerow(data_dict[4])

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    arg = sys.argv[1:]
    file_format = 'svg'
    dir_path = 'Graph_image'
    write_data = None
    main(arg, file_format, dir_path, write_data)
