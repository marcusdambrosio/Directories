import numpy as np
import pandas as pd
import sys,os,time

def add_id_col():
    master = pd.read_excel('new_beekeep_master.xlsx')
    id = pd.read_csv('leadID.csv')
    master['corrID'] = np.zeros_like(master['Name and Business'])
    corrDict = {}
    for i in id['Id']:
        fName = id[id['Id'] == i].FirstName.values[0]
        lName = id[id['Id'] == i].LastName.values[0]
        if type(fName) != str and type(lName) != str:
            continue
        elif type(fName) != str:
            fName = ''
        elif type(lName) != str:
            lName = ''

        corrDict[fName + ' ' + lName] = i

    print('first loop finished')
    counter = 0
    for row in master.iterrows():
        i , row = row

        for name,ID in corrDict.items():
            if name in row['Name and Business']:
                master.loc[i, 'corrID'] = ID

    master.to_excel('new_beekeep_masterIDs.xlsx', index = False)


def add_tasks():
    master = pd.read_excel('new_beekeep_masterIDs.xlsx')
    master['Description'] = np.zeros_like(master['Name and Business'])
    master['OwnerID'] = np.zeros_like(master['Name and Business'])
    tasks = pd.read_csv('taskFile.csv')
    leadData = pd.read_csv('leadID.csv')

    failCount = 0
    # for row in tasks.iterrows():
    #     i , row = row
    #     try:
    #         master.loc[master[master['corrID'] == row['WhoId']].index, 'Description'] = row['Description']
    #         master.loc[master[master['corrID'] == leadData.loc[i, 'Id']].index, 'OwnerId'] = leadData.loc[i, 'OwnerId']
    #
    #     except:
    #         failCount += 1

    for row in leadData.iterrows():
        i , row = row
        try:
            master.loc[master[master['corrID'] == leadData.loc[i, 'Id']].index, 'OwnerId'] = leadData.loc[i, 'OwnerId']
            master.loc[master[master['corrID'] == leadData.loc[i, 'Id']].index, 'LeadSource'] = leadData.loc[i, 'LeadSource']
            master.loc[master[master['corrID'] == leadData.loc[i, 'Id']].index, 'Status'] = leadData.loc[i, 'Status']

        except:
            failCount += 1
    print(failCount)
    master.drop(['Phone 3', 'Phone 4', 'Email 2', 'ID', 'Description'], axis = 1, inplace = True)
    master.rename(columns = {'Email 1' : 'Email', 'Notes': 'Description'}, inplace = True)
    master.to_excel('new_beekeep_master_tasks.xlsx', index = False)



def format_file():
    master = pd.read_csv('beekeep_master_uploadformat.csv')
    companyIdentifiers = ['inc', 'llc', 'honey', 'farm', 'apiary', 'bee']
    master['Company'] = np.zeros_like(master['Name and Business'])
    identified = 0
    counter = 0
    for i in master.index:
        if master.loc[i, 'Email'] == 'None':
            master.loc[i, 'Email'] = 'none@gmail.com'

        if type(master.loc[i, 'Hives']) != int:
            try:
                master.loc[i, 'Hives'] = int(master.loc[i, 'Hives'])
            except:
                master.loc[i, 'Hives'] = 0

        if '--' not in master.loc[i, 'Name and Business']:
            master.loc[i, 'Company'] = master.loc[i, 'Name and Business']
            master.loc[i, 'Name and Business'] = master.loc[i, 'Name and Business']

        else:
            nb1, nb2 = [c.strip().lower() for c in master.loc[i, 'Name and Business'].split('--')]
            for id in companyIdentifiers:
                if len(nb1) > 40:
                    if nb1 == nb2:
                        master.loc[i, 'Company'] = nb1
                        master.loc[i, 'Name and Business'] = 'CHECK COMPANY'
                    else:
                        master.loc[i, 'Company'] = nb1
                        master.loc[i, 'Name and Business'] = nb2
                    break
                elif len(nb2) > 40:
                    if nb1 == nb2:
                        print(nb1,nb2)
                        master.loc[i, 'Company'] = nb2
                        master.loc[i, 'Name and Business'] = 'CHECK COMPANY'
                    else:
                        master.loc[i, 'Company'] = nb2
                        master.loc[i, 'Name and Business'] = nb1
                    break
                elif id in nb1:
                    identified += 1
                    master.loc[i, 'Company'] = nb1
                    master.loc[i, 'Name and Business'] = nb2
                    break
                elif id in nb2:
                    identified += 1
                    master.loc[i, 'Company'] = nb2
                    master.loc[i, 'Name and Business'] = nb1
                    break
                else:
                    if len(nb1) > 40:
                        master.loc[i, 'Name and Business'] = 'CHECK COMPANY'
                    else:
                        master.loc[i, 'Name and Business'] = nb1
                    master.loc[i, 'Company'] = nb2


    #     if len(master.loc[i, 'Name and Business'] )> 40:
    #         counter += 1
    #         # print(master.loc[i, 'Hives'])
    #         # print('\n\n')
    # print(counter)
    # sys.exit()


    print(f'{identified} rows out of {len(master)} could be identified for name/company difference.')
    master.rename(columns = {'Name and Business':'FirstName', 'Phone 0': 'Phone', 'Phone 1': 'Mobile', 'Phone 2': 'Phone Alt', 'Hives': 'hive_quantity', 'Address': 'Physical Address', 'corrID':'Id'}, inplace = True)
    master['LastName'] = np.zeros_like(master['FirstName'])
    master.to_csv('beekeep_master_FINAL.csv', index = False)

format_file()
