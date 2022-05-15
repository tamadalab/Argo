from os import replace
from pandas.core.arrays import string_
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
import sys
import os
import re
import collections
import fig_process

# データの前処理
def Prep(file):
    csv_input = pd.read_csv(filepath_or_buffer = file, encoding="UTF-8", sep=",")
    list = []
    for i in range(0, len(csv_input.index)):
        list.append(csv_input.iat[i,2]) #list内は日時が降順で格納されている
    c = collections.Counter(list) #辞書型  c = {"~~" : n ,,,}  
    keys = [] # 年数リスト
    values = [] # その年の合計値リスト
    accum = [] # 累計数リスト
    for key, value in zip(c.keys(), c.values()):
        keys.append(key)
        values.append(value)
        if (len(accum) == 0):
            accum.append(int(value))
        else:
            total = int(value) + accum[len(accum)-1]
            accum.append(total)
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
    return keys, values, accum, scale, year

# リポジトリ全体の年数リストを取得
def Scale(year, years):
    for i in range(len(year)):
        if not years:
            years.append(year[i])
        elif year[i] not in years:
            years.append(year[i])
    years = sorted((years))
    return years

# 比較グラフ作成
def Com_Plot(file, keys, accum, scale, years):
    plt.plot(keys, accum, label = file, marker = ".",)
    plt.legend() #ラベルの表示
    plt.title("stargazers")
    plt.xlabel("date")
    plt.grid(alpha = 0.6)

# 推移グラフ作成
def Transition_Plot(file, keys, values, scale, years):
    plt.figure()  # 新しいウィンドウを描画
    plt.plot(keys, values, label = file, marker = ".")
    plt.legend()
    plt.title("Transition graph")
    plt.xlabel("date")
    plt.xticks(scale, years) #年単位ごとの目盛の再描画
    plt.grid(alpha = 0.6)

def main(arg, format, dir_path, write_data):
    plt.rcParams["figure.figsize"] = (8,6)
    figure = plt.figure()  # 新しいウィンドウを描画
    # 年数リストを取得
    years = []
    for i in range(len(arg)):
        file = os.path.join("Extracted data", arg[i], "stargazers/CSV/total.csv")
        dict = Prep(file) #keys, values, accum, scale, year
        years = Scale(dict[4], years)

    # リポジトリの古い順に取得
    files = []
    for i in range(len(arg)):
        file = os.path.join("Extracted data", arg[i], "stargazers/CSV/total.csv")
        dict = Prep(file)
        year = dict[4]
        if year[0] == years[0]:
            files.insert(0,file)  
        else:
            files.append(file)

    # プロット化
    # 比較グラフ
    for i in range(len(files)):
        dict = Prep(files[i]) #keys, values, accum, scale, year
        label = re.findall("a/(.*)/s", str(files[i]))
        label = label[0].strip("[""]")
        if write_data is not None:
            fig_process.Print(label, dict[0], dict[2], write_data)
        Com_Plot(label, dict[0], dict[2], dict[3], dict[4]) #比較グラフ作成関数
        if i == 0:
            plt.xticks(dict[3], dict[4]) #年単位ごとの目盛の再描画
    # 推移グラフ
    for i in range(len(files)):
        dict = Prep(files[i]) #keys, values, accum, scale, years
        label = re.findall("a/(.*)/s", str(files[i]))
        label = label[0].strip("[""]")
        Transition_Plot(label, dict[0], dict[1],dict[3], dict[4]) #推移グラフ作成関数

    # グラフ保存
    fig_process.makedir(dir_path)
    for i in range(len(files)):
        fig_process.savefig(figure, dir_path + '/' + "N_STAR", format)


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
