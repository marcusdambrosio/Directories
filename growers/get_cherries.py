import pandas as pd
#
# master = pd.read_csv('full_master.csv')
# cherries = master[master['Commodity'] == 'CHERRY']


# newCherries = pd.DataFrame()
# for row in cherries.iterrows():
#     i , row = row
#     if str(row['Phone']) == 'nan' and str(row['Alternate Phone']) == 'nan' and str(row['Cell']) == 'nan':
#         continue
#     else:
#         newCherries=newCherries.append(row)
#
#
# newCherries.to_csv('cherry_master.csv', index = False)

data = pd.read_csv('cherry_master.csv')
newDat = pd.DataFrame()
for g in data.groupby('Operator'):
    g, dat = g
    acreage = dat['Size'].sum()
    add = dat.iloc[0,:]
    add['Size'] = acreage
    newDat=newDat.append(add)

newDat.to_csv('cherry_master_shortened.csv', index=False)

