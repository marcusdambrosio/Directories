import pandas as pd
import os, sys, time
import numpy as np
import math
from difflib import SequenceMatcher as sm
import datetime as dt



def old_crm():
    os.chdir(r'C:\Users\marcu\PycharmProjects\directories\growers')
    master = pd.read_excel('full_master.xlsx')
    master = master[master['Commodity'] == 'ALMOND'].reset_index()
    print(len(master))
    newOps = [str(c).upper() for c in master['Operator']]
    newAgent = [str(c).upper() for c in master['Agent Name']]
    master['Name'] = [0]*len(master)

    old = pd.read_csv('../beekeepers/old_crm.csv')
    oldOps = [str(c).upper() for c in old['Company']]
    oldNames = [str(c).upper() for c in old['Name']]

    updated = 0
    for i, origOp in enumerate(oldOps):
        op = origOp.upper()
        # if op in newOps or op in newAgent:
        print(i)
        tic = dt.datetime.today()
        for n, new in enumerate(newOps):
            if sm(None, op, new).ratio() > .8 or sm(None, op, newAgent[n]).ratio() > .8:
                updated += 1
                currName = oldNames[i]
                curr = old[(old['Name']).apply(lambda x: str(x).upper()) == currName]
                phones, email = curr[['Phone', 'MobilePhone', 'Phone_Alt__c', 'cell__c']].values.tolist()[0], curr['Email']
                phones = [p.replace('(','').replace(')','').replace('-', '').replace(' ', '') for p in phones if type(p) == str]
                # if op in newOps:
                #     ind = master[master['Operator'] == origOp].index[0]
                # else:
                #     ind = master[master['Agent Name'] == origOp].index[0]
                ind = n

                newPhones = [p.replace('(','').replace(')','').replace('-', '').replace(' ', '') for p in master.loc[ind, ['Phone', 'Alternate Phone', 'Cell', 'Fax']].values.tolist() if type(p) == str]
                phones = pd.Series(newPhones + phones).unique().tolist()
                if len(phones)>4:
                    phones = phones[:4]
                phones += [0]*(4-len(phones))
                master.loc[ind, ['Phone', 'Alternate Phone', 'Cell', 'Fax']] = phones
                master.loc[ind, 'Name'] = currName

            # elif oldNames[i] in newOps or oldNames[i] in newAgent:
            elif sm(None, oldNames[i], new).ratio() > .8 or sm(None, oldNames[i], newAgent[n]).ratio() > .8:
                updated += 1
                currName = oldNames[i]
                curr = old[(old['Name']).apply(lambda x: str(x).upper()) == currName]
                phones, email = curr[['Phone', 'MobilePhone', 'Phone_Alt__c', 'cell__c']].values.tolist()[0], curr['Email']
                phones = [p.replace('(','').replace(')','').replace('-', '').replace(' ', '') for p in phones if type(p) == str]
                # if oldNames[i] in newOps:
                #     ind = master[master['Operator'] == old.loc[i, 'Name']].index[0]
                # else:
                #     ind = master[master['Agent Name'] == old.loc[i, 'Name']].index[0]
                ind = n
                # ind = master[master['Operator'] == op].index
                newPhones = [p.replace('(','').replace(')','').replace('-', '').replace(' ', '') for p in master.loc[ind, ['Phone', 'Alternate Phone', 'Cell', 'Fax']].values.tolist() if type(p) == str]
                phones = pd.Series(newPhones + phones).unique().tolist()
                if len(phones)>4:
                    phones = phones[:4]
                phones += [0]*(4-len(phones))

                master.loc[ind, ['Phone', 'Alternate Phone', 'Cell', 'Fax']] = phones
                master.loc[ind, 'Name'] = currName
        print(dt.datetime.today() - tic)
    master.to_excel('full_master_updated.xlsx', index = False)
    print(f'{updated} contacts updated')

# old_crm()


# os.chdir(r'C:\Users\marcu\PycharmProjects\directories\growers')
#
# dat = pd.read_csv('old_crm.csv')
# dat['Name'] = [0]*len(dat)
#
# for line in dat.iterrows():
#     i, row = line
#     if row['FirstName'] == row['LastName']:
#         name = str(row['FirstName'])
#     else:
#         name = str(row['FirstName']) + ' ' + str(row['LastName'])
#     dat.loc[i , 'Name'] = name
#
# dat.to_csv('old_crm.csv', index = False)
