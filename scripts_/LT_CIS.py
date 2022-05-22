from os import close, replace
from pandas.core.arrays import string_
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys
import os
import re
import collections
import fig_process

# データの前処理
def Prep(file):
    csv_input = pd.read_csv(filepath_or_buffer = file, encoding="UTF-8", sep=",")
    create_list = []
    close_list = []
    temp_list = [0,0]
    date_list = []
    dt_now = datetime.datetime.now()
    dt_YearMonth = str(dt_now.year) + "-" + str(dt_now.month) + "/" + str(dt_now.day)

    for i in range(0, len(csv_input.index)):
        create_list.append(csv_input.iat[i,1]) 
        create = csv_input.iat[i,1]
        if isinstance(csv_input.iat[i,0], float): # closeされていないときは現在時刻(YYYY-MM/DD)を格納
            close_list.append(dt_YearMonth)
            close = dt_YearMonth
        else:
            close_list.append(csv_input.iat[i,0])
            close = csv_input.iat[i,0]
        date_list.append([create, close])
    date_list = sorted(date_list, key=lambda x: datetime.date(datetime.datetime.strptime(x[0], '%Y-%m/%d').year, datetime.datetime.strptime(x[0], '%Y-%m/%d').month, datetime.datetime.strptime(x[0], '%Y-%m/%d').day))
    create_list = sorted(create_list, key=lambda x: datetime.date(datetime.datetime.strptime(x, '%Y-%m/%d').year, datetime.datetime.strptime(x, '%Y-%m/%d').month, datetime.datetime.strptime(x, '%Y-%m/%d').day))
    c = collections.Counter(create_list) #辞書型  c = {"~~" : n ,,,} 
    keys = []
    diff_date = Diff(dt_YearMonth, create_list[0])
    diff = 12 * diff_date[0] + diff_date[1]
    year = create_list[0][:4]
    create = re.findall(r"\d+", create_list[0])
    for i in range(diff+1):
        if i == 0:
            keys.append(str(create[0]) + "-" + str(create[1]))
            month = int(re.findall('-(.*)/', create_list[0])[0])
        else:
            keys.append(str(year) + "-" + str(month))
        
        if month == 12:
            year = int(year) + 1
            month = 1
        else:
            month = int(month) + 1

    #年単位での目盛位置の取得
    scale = []
    scale.append(0)
    year = []
    year.append(int(keys[0][:4]))
    for i in range(1, len(keys)):
        if keys[i].endswith("-1"):
            scale.append(i)
            if keys[i][:4] not in year:
                year.append(int(keys[i][:4]))

    # 種類別各月の取得
    createdAt = []
    for key, value in zip(c.keys(), c.values()):
        createdAt.append(key)

    createdAt = []
    i = 0
    std = 0
    for key in c.keys():
        date = re.findall(r"\d+", key)
        createdAt.append(date[0] + "-" + date[1])

    createdlist = []
    for cread in createdAt:
        if cread not in createdlist:
            createdlist.append(cread)

    print(createdlist)
    # Issue生存時間の取得
    livetime_list = LiveTime(date_list)
    return createdlist, livetime_list, scale, year


def LiveTime(date_list):
    livetime_list = []
    for i in range(len(date_list)):
        diff_date = Diff(date_list[i][1], date_list[i][0])
        create_date = re.findall(r"\d+", date_list[i][0])
        livetime = (diff_date[0] * 365) + (diff_date[1] * 31) + (diff_date[2])
        if i == 0:
            std_month = 0
            num_month = 0
            livetime_total = livetime
            temp_date = re.findall(r"\d+", date_list[i][0])
        elif i == len(date_list)-1:
                try:
                    num_date = livetime_total / num_month
                except ZeroDivisionError:
                    num_date = livetime_total
                livetime_list.append(num_date)
        else:
            if re.findall('-(.*)/', date_list[i][0])[0] == re.findall('-(.*)/', date_list[i-1][0])[0]:
                livetime_total = livetime_total + livetime
                num_month = num_month + 1
            else:
                std_month = std_month + 1
                try:
                    num_date = livetime_total / num_month
                except ZeroDivisionError:
                    num_date = livetime_total
                livetime_list.append(num_date)
                num_month = 0
                temp_date = diff_date
    return livetime_list



# x軸目盛リスト作成
def Xticks(dt_now, first_create):
    diff_date = Diff(dt_now, first_create)
    diff = 12 * diff_date[0] + diff_date[1]
    values = []
    for i in range(diff+1):
        values.insert(i,0)
    return values

# 指定日時とfirst_createtimeの期間差(月数)を求める
def Diff(now_create, first_create):
    create = re.findall(r"\d+", first_create)
    close = re.findall(r"\d+", now_create)
    year = int(close[0]) - int(create[0])
    month = int(close[1]) - int(create[1])
    day = int(close[2]) - int(create[2])
    return year, month, day

# 比較グラフの出力
def Com_Plot(file, keys, values):
    plt.plot(keys, values, label = file, marker = ".",)
    plt.legend() #ラベルの表示
    plt.title("LT_CIS")
    plt.xlabel("date")
    plt.ylabel("Live_time(day)")
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
            fig_process.Print(label, dict[0], dict[1])
        Com_Plot(label, dict[0], dict[1]) #比較グラフ作成関数
        if i == 0:
            plt.xticks(dict[2], dict[3]) #年単位ごとの目盛の再描画

    # グラフ保存
    fig_process.makedir(dir_path)
    for i in range(len(files)):
        fig_process.savefig(figure, dir_path + '/' + "LT_CIS", format)

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