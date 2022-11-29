from os import replace
import pandas as pd
import sys
import os
import csv

def main(metrics, month):
    ## csvデータ読み込み
    file = os.path.join("cache", metrics+".csv")
    csv_input = pd.read_csv(filepath_or_buffer = file, encoding="UTF-8", sep=",")
    monthly_data = []
    for i in range(0, len(csv_input.values[0])): # 列数取得
        if i == 0:
            ripository = (csv_input.iat[20,i])
        else:
            monthly_data.append(float(csv_input.iat[20,i]))
    
    ## 係数計算
    coeff_data = []
    print(len(monthly_data))
    index = 0
    for i in range(0, len(monthly_data)):
        if len(monthly_data) <= index+month:
            coeff_data.append((monthly_data[len(monthly_data)-1] - monthly_data[index]) / month)
            break
        else:
            coeff_data.append((monthly_data[index+month] - monthly_data[index]) / month)
            index = index + month
    print(coeff_data)
    
    # csvデータ出力
    with open(os.path.join("cache/coeff_data/",ripository,metrics+".csv"), 'w', newline = '') as csvFile:
        csvwriter = csv.writer(csvFile, delimiter=',',quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writerow(coeff_data)
    
if __name__ == "__main__":
    arg = sys.argv   
    metrics = arg[1]
    month = arg[2]
    main(metrics, int(month))
