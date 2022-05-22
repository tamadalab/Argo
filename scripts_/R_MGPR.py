from os import replace
from pandas.core.arrays import string_
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
import os
import re
import collections
import fig_process
import itertools

# データの前処理
def Prep(file):
    csv_input = pd.read_csv(filepath_or_buffer = file, encoding="UTF-8", sep=",")
    create_list = []
    close_list = []
    mergetime_list = []
    merge_list = []
    dt_now = datetime.datetime.now()
    dt_YearMonth = str(dt_now.year) + "-" + str(dt_now.month)

    # cratedAt, closedAt, mergedAtの読み込み，取得
    for i in range(0, len(csv_input.index)):
        create_list.append(re.findall("(.*)/", csv_input.iat[i,1]))
        merge_list.append(csv_input.iat[i,2])
        if isinstance(csv_input.iat[i,0], float): # closeされていないときは現在時刻(YYYY-MM)を格納
            close_list.append(dt_YearMonth)
        else:
            close_list.append(re.findall("(.*)/",csv_input.iat[i,0]))
        if isinstance(csv_input.iat[i,3], float): # mergeされていないときは現在時刻(YYYY-MM)を格納
            mergetime_list.append(dt_YearMonth)
        else:
            mergetime_list.append(re.findall("(.*)/", csv_input.iat[i,3]))
    create_list = list(itertools.chain.from_iterable(create_list)) # itertoolsでcreate_listを平坦化する．
    c = collections.Counter(create_list) # 辞書型  c = {"~~" : n ,,,} 

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
        i = i + 1


    # createdAtの取得
    createdAt = []
    for key, value in zip(c.keys(), c.values()):
        createdAt.append(key)

    # 総プルリクスト数の取得
    accum = [] # 累計数リスト
    for value in c.values():
        if (len(accum) == 0):
            accum.append(int(value))
        else:
            total = int(value) + accum[len(accum)-1]
            accum.append(total)

    # merge判定
    mergeCount = []
    i = 0
    for n in range(len(merge_list)):
        if n == 0:
            temp = create_list[n]
            mergeCount.append(0)
        else:
            if temp != create_list[n]:
                temp = create_list[n]
                mergeCount.append(0)
                i = i + 1
            if merge_list[n] == True:
                mergeCount[i] = mergeCount[i] + 1



    # マージされたプルリクエスト率の取得
    r_mgpr = []
    for accum, value in zip(accum, mergeCount):
        per = (value / accum) * 100
        if per > 100:
            per = 100
        r_mgpr.append(per)

    return createdAt, mergeCount, scale, year, r_mgpr, createdAt



# x軸目盛リスト作成
def Xticks(dt_now, first_create):
    target = "-"
    # Year_difference
    Year = dt_now.year - int(first_create[:4])
    # Month_difference
    idx_create = first_create.find(target)
    create_month = first_create[idx_create+1:]
    Month = dt_now.month - int(create_month)
    diff = 12 * Year + Month

    values = []
    for i in range(diff+1):
        values.insert(i,0)



    return values

# 指定日時とfirst_createtimeの期間差(月数)を求める
def Diff(now_create, first_create):
    target = "-"
    # Year_difference
    Year = int(now_create[:4]) - int(first_create[:4])
    # Month_difference
    idx_now = now_create.find(target)
    now = now_create[idx_now+1:]
    idx_first = first_create.find(target)
    first = first_create[idx_first+1:]
    Month = int(now) - int(first)
    diff = 12 * Year + Month
    return diff


def Com_Plot(file, keys, r_ris):
    plt.plot(keys, r_ris, label = file, marker = ".",)
    plt.legend() # ラベルの表示
    plt.title("R_MGPR")
    plt.xlabel("date")
    plt.ylabel("percent")
    plt.grid(alpha = 0.6)

# リポジトリ全体の年数リストを取得
def Scale(year, years):
    for i in range(len(year)):
        if not years:
            years.append(year[i])
        elif year[i] not in years:
            years.append(year[i])
    years = sorted((years))
    return years


def main(arg, format, dir_path, write_data):
    plt.rcParams["figure.figsize"] = (8,6)
    figure = plt.figure()  # 新しいウィンドウを描画

    # リポジトリの古い順に取得
    years = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "pullRequests/CSV/total.csv")
        dict = Prep(file)
        years = Scale(dict[3], years)

    # リポジトリの古い順に取得
    files = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "pullRequests/CSV/total.csv")
        dict = Prep(file)
        year = dict[3]
        if year[0] == years[0]:
            files.insert(0,file)  
        else:
            files.append(file)

    # plot
    for i in range(len(files)):
        dict = Prep(files[i]) # keys, values, scale, year, r_ris
        label = (re.findall("e/(.*)/p", str(files[i])))
        label = label[0].strip("[""]")
        if write_data is not None:
            fig_process.Print(label, dict[4], dict[5], write_data)
        Com_Plot(label, dict[0], dict[4]) # 比較グラフ作成関数
        if i == 0:
            plt.xticks(dict[2], dict[3]) # 年単位ごとの目盛の再描画

    # グラフ保存
    fig_process.makedir(dir_path)
    for i in range(len(files)):
        fig_process.savefig(figure, dir_path + '/' + "R_MGPR", format)

    # グラフ描画
    plt.tight_layout() # グラフ位置の調整
    plt.show()

if __name__ == "__main__":
    arg = sys.argv   ## owner/repositoryはrepository[1]以降に格納
    arg.pop(0)
    format = 'svg'
    dir_path = 'Graph_image'
    write_data = None
    main(arg, format, dir_path, write_data)