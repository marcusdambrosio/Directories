import pandas as pd
import sys,os,time
import numpy as np

try:
    os.mkdir('brokenleads_beek')
except:
    pass
def pull_broken():
    dat=pd.read_csv('lead_1122.csv')
    dat = dat[dat['Industry']=='Beekeeper']
    broken = dat[dat['Status']=='Broken']

    noNum = pd.DataFrame()
    for row in dat.iterrows():
        i,row = row
        if str(row['Phone']) == 'nan':
            noNum=noNum.append(row)
    broken.to_csv('brokenleads_beek/broken.csv', index=False)
    noNum.to_csv('brokenleads_beek/nonumber.csv',index=False)

# pull_broken()

def fill_broken():
    broken = pd.read_csv('brokenleads_beek/nonumber.csv')
    old = pd.read_csv('old_crm.csv')

    for row in broken.iterrows():
        i,row=row
        b = row['Company']
        temp = old[old['Company']==b]
        try:
            broken.loc[i,'Phone']=str(temp['Phone'][temp.index[0]])
        except:
            pass
    broken = broken[broken['Phone'] != 'nan']

    broken.to_csv('brokenleads_beek/nonum_filled.csv',index=False)
# fill_broken()

def fill_nonmum():
    nonum = pd.read_csv('brokenleads_beek/nonumber.csv')
    oldsheet = pd.read_csv('old_bekeep_list_allnumbers_fromgoogdrive.csv')

    for row in nonum.iterrows():
        i, row = row
        for row2 in oldsheet.iterrows():
            n, row2 = row2
            if row['Company'].lower() in row2['Name and Business']:
                phones = [c+',' for c in row2[['Phone 0','Phone 1', 'Phone 2']].tolist()
                          if c != row2[['Phone 0','Phone 1', 'Phone 2']].tolist()[-1]]
                phones = ''.join(phones)
                print(phones)
                nonum.loc[i, 'Phone'] = phones
    nonum.to_csv('brokenleads_beek/nonumber_newfill.csv', index = False)

def fill_nonum_oldestcrm():
    nonum = pd.read_csv('brokenleads_beek/nonumber.csv')
    oldsheet = pd.read_csv('oldest_crm.csv')

    for row in nonum.iterrows():
        i, row = row
        for row2 in oldsheet.iterrows():
            n, row2 = row2
            if row['Company'].lower() in row2['Company']:
                phones = [str(c) + ',' for c in row2[['Phone', 'MobilePhone', 'Phone_Alt__c', 'cell__c']].tolist()
                          if c != row2[['Phone', 'MobilePhone', 'Phone_Alt__c', 'cell__c']].tolist()[-1]]
                phones = ''.join(phones)
                print(phones)
                nonum.loc[i, 'Phone'] = phones
    nonum.to_csv('brokenleads_beek/nonumber_newfill2.csv', index=False)

fill_nonum_oldestcrm()

sys.exit()

