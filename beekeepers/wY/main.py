import sys

import pandas as pd


def main():
    dat = pd.read_csv('raw_table.csv')
    master = pd.DataFrame()
    print(len(dat.groupby('Owner Name')))
    for g in dat.groupby('Owner Name'):
        i, g = g
        hives = g['Number of Hives'].sum()
        temp = g.iloc[0,:]
        temp['hives'] = hives
        master = master.append(temp)

    master.to_csv('WY_master1.csv', index=False)


if __name__ == '__main__':
    main()