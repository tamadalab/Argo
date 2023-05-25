import pandas as pd
import sys
import os
import csv


def main(repository, metrics, period):
    # csvデータ読み込み
    file = os.path.join("cache", repository, metrics, "plot_data.csv")
    csv_input = pd.read_csv(file, encoding="UTF-8", sep=",")
    monthly_data = [float(csv_input.iat[0, i]) for i in range(len(csv_input.values[0]))]

    # 係数計算
    month = []
    coeff_data = []
    index = 0
    for i in range(len(monthly_data)):
        if len(monthly_data) <= index + period:
            coeff_data.append((monthly_data[len(monthly_data) - 1] - monthly_data[index]) / period)
            break
        else:
            coeff_data.append((monthly_data[index + period] - monthly_data[index]) / period)
            index = index + period
        month.append(csv_input.columns[index])
    month.append(csv_input.columns[len(monthly_data) - 1])
    print(coeff_data)

    # csvデータ出力
    with open(os.path.join("cache", repository, metrics, "coeff.csv"), 'a', newline='') as csvFile:
        csvwriter = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        csvwriter.writerow(month)
        csvwriter.writerow(coeff_data)


if __name__ == "__main__":
    repository, metrics, period = sys.argv[1], sys.argv[2], int(sys.argv[3])
    main(repository, metrics, period)
