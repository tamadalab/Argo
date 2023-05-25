import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
import os
import re
import collections
import fig_process
import csv


# データの前処理
def prep(file):
    csv_input = pd.read_csv(filepath_or_buffer=file, encoding="UTF-8", sep=",")
    create_list = []
    mergetime_list = []
    dt_now = datetime.datetime.now()
    dt_YearMonth = str(dt_now.year) + "-" + str(dt_now.month) + "/" + str(dt_now.day)

    for i in range(0, len(csv_input.index)):
        create_list.append(csv_input.iat[i, 2])
        if isinstance(csv_input.iat[i, 6], float):  # mergeされていないときは現在時刻(YYYY-MM/DD)を格納
            mergetime_list.append(dt_YearMonth)
        else:
            print(csv_input.iat[i, 6])
            mergetime_list.append(csv_input.iat[i, 6])

    # create, closedate取得
    keys = []
    diff = diff(dt_YearMonth, create_list[0])
    year = create_list[0][:4]
    for i in range(diff + 1):
        if i == 0:
            keys.append(re.findall('(.*)/', create_list[0])[0])
            month = int(re.findall('-(.*)/', create_list[0])[0])
        else:
            keys.append(str(year) + "-" + str(month))

        if month == 12:
            year = int(year) + 1
            month = 1
        else:
            month = int(month) + 1

    # create_dateの取得
    c = collections.Counter(create_list)  # 辞書型  c = {"~~" : n ,,,}
    test = []
    i = 0
    std = 0
    for key in c.keys():
        if i == 0:
            test.append(re.findall('(.*)/', key)[0])
        else:
            if re.findall('(.*)/', key)[0] != test[std]:
                test.append(re.findall('(.*)/', key)[0])
                std = std + 1
        i = i + 1

    # PullRequest生存時間の取得
    livetime_list = livetime(create_list, mergetime_list)

    # 残PullRequest期間の取得
    rem_issue_prd = []
    for i in range(len(create_list)):
        # Year_difference
        Year = int(mergetime_list[i][:4]) - int(create_list[i][:4])
        # Month_difference
        Month = int(re.findall('-(.*)/', mergetime_list[i])[0]) - int(re.findall('-(.*)/', create_list[i])[0])
        diff = 12 * Year + Month
        rem_issue_prd.append(diff)
    values = xticks(dt_YearMonth, create_list[0])

    # 月毎の残イシュー数をカウント, Scaleリストに格納する
    for i in range(len(create_list)):
        start_num = diff(create_list[i], create_list[0])
        for n in range(rem_issue_prd[i] + 1):
            values[start_num] = values[start_num] + 1
            start_num = start_num + 1

    # 年単位での目盛位置の取得
    scale = []
    scale.append(0)
    year = []
    year.append(int(keys[0][:4]))
    for i in range(1, len(keys)):
        if keys[i].endswith("-1"):
            scale.append(i)
            if keys[i][:4] not in year:
                year.append(int(keys[i][:4]))
    return test, livetime_list, scale, year


def livetime(create_list, close_list):
    livetime_list = []
    target = "/"
    for i in range(len(create_list)):
        year = int(close_list[i][:4]) - int(create_list[i][:4])
        month = int(re.findall('-(.*)/', close_list[i])[0]) - int(re.findall('-(.*)/', create_list[i])[0])
        create_idx = create_list[i].find(target)
        create_r = create_list[i][create_idx + 1:]
        close_idx = close_list[i].find(target)
        close_r = close_list[i][close_idx + 1:]
        day = int(close_r) - int(create_r)
        livetime = (year * 360) + (month * 31) + (day)
        if i == 0:
            std_month = 0
            livetime_list.append(livetime)
        else:
            if re.findall('-(.*)/', create_list[i])[0] == re.findall('-(.*)/', create_list[i - 1])[0]:
                livetime_list[std_month] = livetime_list[std_month] + livetime
            else:
                std_month = std_month + 1
                livetime_list.append(livetime)
    return livetime_list


# x軸目盛リスト作成
def xticks(dt_now, first_create):
    # Year_difference
    Year = int(dt_now[:4]) - int(first_create[:4])
    # Month_difference
    Month = int((re.findall('-(.*)/', dt_now))[0]) - int((re.findall('-(.*)/', first_create))[0])
    diff = 12 * Year + Month
    values = []
    for i in range(diff + 1):
        values.insert(i, 0)
    return values


# 指定日時とfirst_createtimeの期間差(月数)を求める
def diff(now_create, first_create):
    # Year_difference
    Year = int(now_create[:4]) - int(first_create[:4])
    # Month_difference
    Month = int(re.findall('-(.*)/', now_create)[0]) - int(re.findall('-(.*)/', first_create)[0])
    diff = 12 * Year + Month
    return diff


# 比較グラフの出力
def com_plot(file, keys, values):
    plt.plot(keys, values, label=file, marker=".")
    plt.legend()  # ラベルの表示
    plt.title("LT_PR")
    plt.xlabel("date")
    plt.ylabel("Live_time(day)")
    plt.grid(alpha=0.6)


# リポジトリ全体の年数リストを取得
def scale(year, years):
    for i in range(len(year)):
        if not years:
            years.append(year[i])
        elif year[i] not in years:
            years.append(year[i])
    years = sorted((years))
    return years


def main(arg, file_format, dir_path, write_data):
    plt.rcParams["figure.figsize"] = (8, 6)
    figure = plt.figure()  # 新しいウィンドウを描画

    # リポジトリの古い順に取得
    years = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "pullRequests/CSV/total.csv")
        dict_data = prep(file)
        years = scale(dict_data[3], years)

    # リポジトリの古い順に取得
    files = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "pullRequests/CSV/total.csv")
        dict_data = prep(file)
        year = dict_data[3]
        if year[0] == years[0]:
            files.insert(0, file)
        else:
            files.append(file)

    for i in range(len(files)):
        dict_data = prep(files[i])  # keys, values, accum, scale, year
        label = re.findall("e/(.*)/p", str(files[i]))
        label = label[0].strip("[""]")
        if write_data is not None:
            fig_process.print_data(label, dict_data[0], dict_data[1], write_data)
        com_plot(label, dict_data[0], dict_data[1])  # 比較グラフ作成関数
        if i == 0:
            plt.xticks(dict_data[2], dict_data[3])  # 年単位ごとの目盛の再描画

    # グラフ保存
    fig_process.make_dir(dir_path)
    for i in range(len(files)):
        fig_process.save_fig(figure, dir_path + '/' + "LT_PR", file_format)
        fig_process.make_dir("cache/" + arg[i] + "/" + "LT_PR")
        file = os.path.join("cache", arg[i], "LT_PR/plot_data.csv")
        with open(file, "a") as f:
            writer = csv.writer(f)
            writer.writerow(dict_data[0])
            writer.writerow(dict_data[1])

    # グラフ描画
    plt.tight_layout()  # グラフ位置の調整
    plt.show()


if __name__ == "__main__":
    arg = sys.argv  ## owner/repositoryはrepository[1]以降に格納
    arg.pop(0)
    dir_path = 'Graph_image'
    write_data = None
    main(arg, format, dir_path, write_data)
