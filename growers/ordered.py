import pandas as pd
import sys,os,time

dat = pd.read_csv('oldCRM_mailing_list.csv')
oldDat= pd.read_csv('old_mailing_list.csv')

oldst = oldDat['Mailing Address']
n = 0
notin = []
d = [str(c).strip().lower() for c in dat['Street']]
for row in oldDat.iterrows():
    i , row = row
    fname, lname = 'none', 'none'
    if str(row['Mailing Address']).strip().lower() not in d:
        if '"' in row['Agent Name']:
            lname = row['Agent Name'].split(',')[0].strip().strip('"')
            fname = row['Agent Name'].split(',')[1].strip().strip('"')

        dat = dat.append({'FirstName':fname,
                          'LastName':lname,
                          'Company': row['Agent Name'],
                          'Street' : row['Mailing Address'],
                          'City': row['City'],
                          'State': row['State'],
                          'Zip':row['Zip']}, ignore_index=True)


names = dat['FirstName'] + pd.Series([' ']*len(dat)) + dat['LastName']
print(len(names.unique()))
sys.exit()
dat['FullName'] = names

dat=dat.sort_values(by='FullName')

dat.to_csv('combinedCRM_mailing_list.csv', index = False)


sys.exit()
data = pd.read_excel('full_master.xlsx')

crops = data['Commodity'].tolist()

targets = ['ALMOND', 'CHERRY', 'BLUEBERRY']
master = pd.DataFrame()
for t in targets:
    master = master.append(data[data['Commodity'] == t])
print(len(master))
growers = master['Operator'].unique()
growers = master['Agent Name'].unique()
print(len(growers))
sys.exit()

uniqueMaster = pd.DataFrame()
for grower in growers:
    currDf = master[master['Operator'] == grower]
    # currDf = currDf[currDf['Site Active'] == 'Active']
    try:
        topRow = currDf.iloc[0, :]
        topRow['totalAcres'] = sum(currDf['GIS Acres'])
        uniqueMaster = uniqueMaster.append(topRow)
    except:
        pass


# uniqueMaster = pd.read_excel('unique_grower_master.xlsx')
uniqueMaster.reset_index(drop = True,inplace = True)
uniqueMaster.sort_values(by='totalAcres', ascending=False, inplace = True)
uniqueMaster.to_excel('unique_grower_list2.xlsx', index = False)

