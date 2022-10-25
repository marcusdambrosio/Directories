import os, time, sys
import pandas as pd


def combine():
    master = pd.ExcelFile('All Crops 2021/master.xlsx')
    master = master.parse(master.sheet_names[-1])

    permitNum = ['Permit Number', 'Permit #']
    permitee = ['Operator' ,'Permitee']
    siteID = ['Site-ID', 'Site ID']
    m = ['M', 'Meridian']
    t = ['T' , 'Township']
    r = ['R' , 'Range']
    s = ['S' , 'Section']
    comm = ['Commodity']
    plantedAmt = ['Planted Size', 'Planted Amount']
    plantUnits = ['Planted Units']

    for file in os.listdir('All Crops 2021'):
        if 'master' in file or 'Amador' in file or 'Butte' in file:
            continue
        currDf = pd.ExcelFile(f'All Crops 2021/{file}')
        currDf = currDf.parse(currDf.sheet_names[-1])
        countyName = file.split('Grower')[0].split('grower')[0].replace('County', '').strip()
        currDf['County'] = [countyName] * len(currDf)
        currDict = {}
        for col in currDf.columns:
            if col in master.columns:
                currDict[col] = currDf[col]
            else:
                for category in [permitNum, permitee, siteID, m, t, r, s, comm, plantedAmt , plantUnits]:
                    if col in category:
                        currDict[category[0]] = currDf[col]

        temp = pd.DataFrame.from_dict(currDict)
        master = master.append(temp)
    master.to_excel('full_master.xlsx', index = False)


# combine()


def remove_duplicates():
    master = pd.read_excel('full_master.xlsx')
    names = master['Operator'].unique()

    def list_to_string(list):
        if len(list) == 1:
            return str(list[0])
        else:
            final = ''
            for ele in list:
                final = final + str(ele).strip() + ', '
        return final.strip(', ')
    newMaster = pd.DataFrame(columns = master.columns)
    for name in names:
        subDf = master[master['Operator'] == name]
        print(subDf)
        print(len(subDf))
        print(subDf['Permit Number'])
        sys.exit()

        crops, counties, permits = subDf['Commodity'].unique(), subDf['County'].unique(), subDf['Permit Number'].unique()
        crops = list_to_string(crops)
        counties = list_to_string(counties)
        permits = list_to_string(permits)


        try:
            appendRow = subDf[subDf['County'] != 'Kern'].iloc[0, :]
        except:
            appendRow = subDf.iloc[0,:]
        appendRow['Commodity'] = crops
        appendRow['County'] = counties
        appendRow['Permit Number'] = permits
        # counter = 0
        #
        # while appendRow['County'] in ['Kern' ,'Placer']:
        #     counter += 1
        #     appendRow = subDf.iloc[0, :]
        newMaster=newMaster.append(appendRow)

    newMaster.to_excel('unique_grower_master.xlsx', index = False)

def remove_duplicates_allRows():
    master = pd.read_excel('full_master.xlsx')
    names = master['Operator'].unique()

    def list_to_string(list):
        if len(list) == 1:
            return str(list[0])
        else:
            final = ''
            for ele in list:
                final = final + str(ele).strip() + ', '
        return final.strip(', ')
    newMaster = pd.DataFrame(columns = master.columns)
    for name in names:
        subDf = master[master['Operator'] == name]
        countyGroups = subDf.groupby('County')
        cropGroups = subDf.groupby('Commodity')

        for county, df in countyGroups:
            newMaster = newMaster.append(df.iloc[0,:])
        for crop, cdf in cropGroups:
            newMaster= newMaster.append(cdf.iloc[0,:])

    newMaster.to_excel('unique_grower_master_allRows.xlsx', index = False)


dat = pd.read_csv('unique_grower_master_allRows.xlsx')
print(dat['Commodity'].unique())
