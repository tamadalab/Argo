from os import replace
from urllib.response import addinfo
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
    additions = []
    deletions = []
    create_list = []
    dt_now = datetime.datetime.now()
    dt_YearMonth = str(dt_now.year) + "-" + str(dt_now.month)

    # cratedAt, closedAtの読み込み
    for i in range(0, len(csv_input.index)):
        additions.append(csv_input.iat[i,0])
        deletions.append(csv_input.iat[i,3])
        create_list.append(re.findall("(.*)/", csv_input.iat[i,2]))

    create_list = list(itertools.chain.from_iterable(create_list)) # itertoolsでcreate_listを平坦化する．
    print(create_list)
    c = collections.Counter(create_list) #辞書型  c = {"~~" : n ,,,} 

    #年単位での目盛位置の取得
    year = []
    scale = []
    createdAt = []
    code_amount = []
    amount = 0
    i = 0
    n = 0
    l = 1
    for key, value in zip(c.keys(), c.values()):
        createdAt.append(key)
        if not year:
            year.append(key[:4])
            scale.append(i)
        elif key[:4] not in year:
            year.append(key[:4])
            scale.append(i)
        i = i + 1
        # コードの増減計算
        for m in range(value):
            temp = additions[n] + deletions[n]
            value_tmp = value 
            amount += temp
            n = n + 1
        code_amount.append(amount)
    return createdAt, code_amount, scale, year



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

def Com_Plot(file, keys, r_ris):
    plt.plot(keys, r_ris, label = file, marker = ".",)
    plt.legend(fontsize = 25) #ラベルの表示
    plt.title("N_MGCL")
    plt.xlabel("date")
    plt.ylabel("code")
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
    plt.rcParams["figure.figsize"] = (15,10)
    plt.rcParams["font.size"] = (20)
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

    for i in range(len(files)):
        dict = Prep(files[i]) #keys, values, scale, year, r_ris
        label = re.findall("e/(.*)/p", str(files[i]))
        label = label[0].strip("[""]")
        if write_data is not None:
            fig_process.Print(label, dict[0], dict[1], write_data)
        Com_Plot(label, dict[0], dict[1]) #比較グラフ作成関数
        if i == 0:
            plt.xticks(dict[2], dict[3]) #年単位ごとの目盛の再描画

    # グラフ保存
    fig_process.makedir(dir_path)
    for i in range(len(files)):
        fig_process.savefig(figure, dir_path + '/' + "N_MGCL", format)


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
