import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
import os
import re
import collections
import itertools
import numpy as np
import csv

import fig_process


# データの前処理
def prep(file):
    csv_input = pd.read_csv(filepath_or_buffer=file, encoding="UTF-8", sep=",")
    create_list = []
    mergetime_list = []
    merge_list = []
    dt_now = datetime.datetime.now()
    dt_YearMonth = f"{dt_now.year}-{dt_now.month}"
    totalCount_list = []
    participant_list = []

    # cratedAt, merged, mergedAt, participant_totalCountの読み込み，取得
    for i in range(len(csv_input.index)):
        create_list.append(re.findall("(.*)/", csv_input.iat[i, 2]))
        merge_list.append(csv_input.iat[i, 4])
        if not isinstance(csv_input.iat[i, 5], float):  # mergeされていないときは現在時刻(YYYY-MM)を格納
            mergetime_list.append(re.findall("(.*)/", csv_input.iat[i, 5]))
            if csv_input.iat[i, 2] is not None:
                participant_list.append(csv_input.iat[i, 6])
    
    # mergetime_listの年代別ソート
    mergetime_list = list(itertools.chain.from_iterable(mergetime_list))  # itertoolsでcreate_listを平坦化する．
    mergetime_list = list(map(lambda s: f"{s}-1", mergetime_list))
    mergetime_list = sorted(mergetime_list, key=lambda x: datetime.date(datetime.datetime.strptime(x, '%Y-%m-%d').year, datetime.datetime.strptime(x, '%Y-%m-%d').month, datetime.datetime.strptime(x, '%Y-%m-%d').day))
    c = collections.Counter(mergetime_list)  # 辞書型  c = {"~~" : n ,,,} 

    # 年単位での目盛位置の取得
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

    # createdAt要素の取得
    mergedAt = list(c.keys())

    # participant_totalCount判定
    mergeCount = []
    i = 0
    count = 0  # 参加者の欠けるマージされたプルリクエスト数カウント変数
    total = 0  # その月のマージされたプルリクエスト数カウント変数
    temp = mergetime_list[0]
    accum = []
    month_total = []
    for i in range(len(participant_list)):
        # 条件文(年月更新)
        if int(participant_list[i]) == 1:
            count += 1
        total += 1
        if temp != mergetime_list[i]:
            accum.append(count)
            month_total.append(total)
            temp = mergetime_list[i]
            count = 0
            total = 0

        # 最終月のカウント数を格納
        if i == len(participant_list) - 1:
            accum.append(count)
            total += 1
            month_total.append(total)

    # マージされたプルリクエスト率の取得
    r_prlp = []
    for count, total in zip(accum, month_total):
        per = (count / total) * 100
        if per > 100:
            per = 100
        r_prlp.append(per)
    
    return mergedAt, mergeCount, scale, year, r_prlp, mergedAt


# x軸目盛リスト作成
def x_ticks(dt_now, first_create):
    target = "-"
    # Year_difference
    Year = dt_now.year - int(first_create[:4])
    # Month_difference
    idx_create = first_create.find(target)
    create_month = first_create[idx_create + 1:]
    Month = dt_now.month - int(create_month)
    diff = 12 * Year + Month

    values = [0] * (diff + 1)

    return values


# 指定日時とfirst_createtimeの期間差(月数)を求める
def diff(now_create, first_create):
    target = "-"
    # Year_difference
    Year = int(now_create[:4]) - int(first_create[:4])
    # Month_difference
    idx_now = now_create.find(target)
    now = now_create[idx_now + 1:]
    idx_first = first_create.find(target)
    first = first_create[idx_first + 1:]
    Month = int(now) - int(first)
    diff = 12 * Year + Month
    return diff


def compare_plot(file, keys, r_mgpr):
    plt.plot(keys, r_mgpr, label=file, marker=".")
    plt.legend()  # ラベルの表示
    plt.title("R_PRLP")
    plt.xlabel("date")
    plt.ylabel("percent")
    plt.grid(alpha=0.6)


# リポジトリ全体の年数リストを取得
def get_years(year, years):
    for i in range(len(year)):
        if not years:
            years.append(year[i])
        elif year[i] not in years:
            years.append(year[i])
    years = sorted(years)
    return years


def main(arg, file_format, dir_path, write_data):
    plt.rcParams["figure.figsize"] = (8, 6)
    figure = plt.figure()  # 新しいウィンドウを描画

    # リポジトリの古い順に取得
    years = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "pullRequests/CSV/total.csv")
        data_dict = prep(file)
        years = get_years(data_dict[3], years)

    # リポジトリの古い順に取得
    files = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "pullRequests/CSV/total.csv")
        data_dict = prep(file)
        year = data_dict[3]
        if year[0] == years[0]:
            files.insert(0, file)
        else:
            files.append(file)

    for i in range(len(files)):
        data_dict = prep(files[i])  # keys, values, scale, year, r_mgpr
        label = re.findall("e/(.*)/p", str(files[i]))
        label = label[0].strip("[""]")
        if write_data is not None:
            fig_process.print_data(label, data_dict[4], data_dict[0], write_data)
        compare_plot(label, data_dict[0], data_dict[4])  # 比較グラフ作成関数
        if i == 0:
            plt.xticks(data_dict[2], data_dict[3])  # 年単位ごとの目盛の再描画

    # グラフ保存
    fig_process.make_dir(dir_path)
    for i in range(len(files)):
        fig_process.savefig(figure, dir_path + '/' + "R_PRLP", file_format)
        fig_process.make_dir("cache/" + arg[i] + "/" + "R_PRLP")
        file = os.path.join("cache", arg[i], "R_PRLP/plot_data.csv")
        with open(file, "w") as f:
            writer = csv.writer(f)
            writer.writerow(data_dict[0])
            writer.writerow(data_dict[4])

    # グラフ描画
    plt.tight_layout()  # グラフ位置の調整
    plt.show()


if __name__ == "__main__":
    arg = sys.argv  # owner/repositoryはrepository[1]以降に格納
    arg.pop(0)
    file_format = 'svg'
    dir_path = 'Graph_image'
    write_data = None
    main(arg, file_format, dir_path, write_data)
