import pandas as pd

data = pd.read_csv('cherry_master.csv')
newDat = pd.DataFrame()
for g in data.groupby('Operator'):
    g, dat = g
    acreage = dat['Size'].sum()
    add = dat.iloc[0,:]
    add['Size'] = acreage
    newDat=newDat.append(add)

newDat.to_csv('cherry_master_shortened.csv', index=False)

