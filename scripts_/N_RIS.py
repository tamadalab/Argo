from os import replace
from socket import close
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
    dt_now = datetime.datetime.now()
    dt_YearMonth = str(dt_now.year) + "-" + str(dt_now.month)
    now_date = []
    now_date.append(dt_YearMonth)


    for i in range(0, len(csv_input.index)):
        create_list.append(re.findall("(.*)/", csv_input.iat[i,1]))
        if isinstance(csv_input.iat[i,0], float): # closeされていないときは現在時刻(YYYY-MM)を格納
            close_list.append(now_date)
        else:
            close_month = re.findall("(.*)/", csv_input.iat[i,0])
            close_list.append(close_month)
    create_list = list(itertools.chain.from_iterable(create_list)) # itertoolsでcreate_listを平坦化する．
    close_list = list(itertools.chain.from_iterable(close_list)) # itertoolsでcreate_listを平坦化する．
    c = collections.Counter(create_list) #辞書型  c = {"~~" : n ,,,} 
    
    # create, closedate取得
    keys = []
    diff = Diff(dt_YearMonth, create_list[0])
    target = "-"
    year = create_list[0][:4]
    for i in range(diff+1):
        if i == 0:
            keys.append(create_list[0])
            idx_create = create_list[0].find(target)
            month = create_list[0][idx_create+1:]
        else:
            keys.append(str(year) + "-" + str(month))
        
        if month == 12:
            year = int(year) + 1
            month = 1
        else:
            month = int(month) + 1

    # 残Issue期間の取得
    remIssue_prd = []
    for i in range(len(create_list)):
        diff = Diff(close_list[i], create_list[i])
        remIssue_prd.append(diff)
    values = Xticks(dt_now, create_list[0])  

    # 月毎の残イシュー数をカウント, Scaleリストに格納する
    for i in range(len(create_list)):
        start_num = Diff(create_list[i], create_list[0])
        print("test")
        print(create_list[i])
        print(create_list[0])
        for n in range(remIssue_prd[i]+1):
            values[start_num] = values[start_num] + 1
            start_num = start_num + 1
        print(values)

    #年単位での目盛位置の取得
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
    return keys, values, scale, year



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


def Com_Plot(file, keys, values):
    plt.plot(keys, values, label = file, marker = ".",)
    plt.legend() #ラベルの表示
    plt.title("N-RIS")
    plt.xlabel("date")
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
        file = os.path.join("cache", arg[i], "issues/CSV/total.csv")
        dict = Prep(file)
        years = Scale(dict[3], years)

    # リポジトリの古い順に取得
    files = []
    for i in range(len(arg)):
        file = os.path.join("cache", arg[i], "issues/CSV/total.csv")
        dict = Prep(file)
        year = dict[3]
        if year[0] == years[0]:
            files.insert(0,file)  
        else:
            files.append(file)

    for i in range(len(files)):
        dict = Prep(files[i]) #keys, values, accum, scale, year
        label = re.findall("e/(.*)/i", str(files[i]))
        label = label[0].strip("[""]")
        if write_data is not None:
            fig_process.Print(label, dict[0], dict[1], write_data)
        Com_Plot(label, dict[0], dict[1]) #比較グラフ作成関数
        if i == 0:
            plt.xticks(dict[2], dict[3]) #年単位ごとの目盛の再描画

    # グラフ保存
    fig_process.makedir(dir_path)
    for i in range(len(files)):
        fig_process.savefig(figure, dir_path + '/' + "N_RIS", format)

    # グラフ描画
    plt.tight_layout() #グラフ位置の調整
    plt.show()


if __name__ == "__main__":
    arg = sys.argv   ## owner/repositoryはrepository[1]以降に格納
    arg.pop(0)
    format = 'svg'
    dir_path = 'Graph_image'
    write_data = None
    main(arg, format, dir_path, write_data)
