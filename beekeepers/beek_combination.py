import pandas as pd
import numpy as np
import os, sys, time
import re
from difflib import SequenceMatcher


def master():
    df = pd.read_excel('sources/beekeeper_master.xlsx')
    return df

def master2():
    df = pd.read_excel('new_beekeep_master.xlsx')
    return df

def master3():
    df = pd.read_excel('testing.xlsx')
    return df

def beekeeper_calls():
    mast = master()
    data = pd.read_excel('sources/beekeeper calls.xlsx')
    data = data[data['name'].notna()]
    data.fillna('None', inplace = True)
    phones = {}
    for row in mast.iterrows():
        i,row = row
        phones[i] = [row[f'Phone {n}'].replace('-', '').strip() for n in range(5)]

    for row in data.iterrows():
        i, row = row
        if type(row['numbers']) != str:
            continue
        newPhones = []
        for num in row['numbers'].split('\n'):
            num = num.replace('-', '').strip()
            newPhones.append(num)
        newPhones = [p for p in newPhones if p != '']
        if len(newPhones[0]) > 14:
            newPhones = newPhones[0].split(' ')
        for count, ph in enumerate(newPhones):
            for key , ph2 in phones.items():
                if ph in ph2: #matching phones
                    ph2 =  [c for c in ph2 if len(c) > 5]
                    final = list(set(newPhones) | set(ph2))
                    for count2, val in enumerate(final):
                        mast.loc[key, f'Phone {count2}'] = val
                    match = True
                    break
                else:
                    match = False


            if not match:
                maxPhones = len(newPhones)

                newPhoneDict = {}
                for i in range(5):
                    if i > maxPhones - 1:
                        newPhoneDict[i] = 'None'
                    else:
                        newPhoneDict[i] = newPhones[i]

                mast = mast.append({'Name and Business' : row['name'],
                                    'ID' : 'None',
                                    'Address': 'possibly in name column',
                                    'Hives' : row['hives'],
                                    'Phone 0': newPhoneDict[0],
                                    'Phone 1': newPhoneDict[1],
                                    'Phone 2': newPhoneDict[2],
                                    'Phone 3': newPhoneDict[3],
                                    'Phone 4': newPhoneDict[4],
                                    'Notes': row['7/28/2020 notes'] + ', ' + row['7/29/2020 notes'] + ', ' + row['8/6/2020 notes'],
                                    'Email 1': row['email']
                                    }, ignore_index = True)

        mast.to_excel('new_beekeep_master.xlsx', index=  False)


def beekeeperz():
    mast = master2()
    data = pd.read_excel('sources/Beekeeperz.xlsx', sheet_name = None)
    '''ND BEEKEEPERS'''
    nd = data['ND BEEKEEPERS']
    nd = nd[nd['Name'].notna()]
    nd.fillna('None', inplace=True)
    phones = {}
    for row in mast.iterrows():
        i,row = row
        phones[i] = [row[f'Phone {n}'].replace('-', '').strip() for n in range(5)]

    for row in nd.iterrows():
        i, row = row
        if type(row['Phone']) != str:
            continue
        newPhones = []
        for num in row['Phone'].split('//'):
            num = num.replace('-', '').strip()
            num = num.replace('(', '').strip()
            num = num.replace(')', '').strip()
            num = re.sub("[^0-9]", "", num)
            newPhones.append(num)
        newPhones = [p for p in newPhones if p != '']
        for altPhone in row['Alt Phone']:
            altPhone = altPhone.replace('-', '').strip()
            altPhone = altPhone.replace('(', '').strip()
            altPhone = altPhone.replace(')', '').strip()
            altPhone = re.sub("[^0-9]", "", altPhone)
            if altPhone not in newPhones and len(altPhone) > 8:
                newPhones.append(altPhone)

        for count, ph in enumerate(newPhones):
            for key, ph2 in phones.items():
                if ph in ph2:  # matching phones
                    ph2 = [c for c in ph2 if len(c) > 5]
                    final = list(set(newPhones) | set(ph2))
                    for count2, val in enumerate(final):
                        mast.loc[key, f'Phone {count2}'] = val
                    match = True
                    break
                else:
                    match = False

            if not match:
                maxPhones = len(newPhones)
                newPhoneDict = {}
                for i in range(5):
                    if i > maxPhones - 1:
                        newPhoneDict[i] = 'None'
                    else:
                        newPhoneDict[i] = newPhones[i]

                mast = mast.append({'Name and Business': row['Name'] + ' -- ' + row['Company'],
                                    'ID': 'None',
                                    'Address': 'None',
                                    'Hives': row['Quantity'],
                                    'Phone 0': newPhoneDict[0],
                                    'Phone 1': newPhoneDict[1],
                                    'Phone 2': newPhoneDict[2],
                                    'Phone 3': newPhoneDict[3],
                                    'Phone 4': newPhoneDict[4],
                                    'Notes': row['WINTER STORAGE BABY'],
                                    'Email 1': row['Email']
                                    }, ignore_index=True)

    mast.to_excel('new_beekeep_master.xlsx', index=  False)
    mast = master2()

    '''ahpa. dont touch'''
    ahpa = data['ahpa. dont touch']
    ahpa = ahpa[ahpa['First Name'].notna()]
    ahpa.fillna('None', inplace=True)
    ahpa['Name'] = ahpa['First Name'] + ' ' + ahpa['Last Name']
    ahpa.drop('First Name', axis = 1, inplace = True)
    ahpa.drop('Last Name', axis = 1, inplace = True)
    for row in ahpa.iterrows():
        i, row = row
        if type(row['Quantity']) != str:
            continue
        newPhones = []
        for num in row['Quantity'].split('//'):
            num = num.replace('-', '').strip()
            num = num.replace('(', '').strip()
            num = num.replace(')', '').strip()
            num = re.sub("[^0-9]", "", num)
            newPhones.append(num)
        newPhones = [p for p in newPhones if p != '']

        for count, ph in enumerate(newPhones):
            for key, ph2 in phones.items():
                if ph in ph2:  # matching phones
                    ph2 = [c for c in ph2 if len(c) > 5]
                    final = list(set(newPhones) | set(ph2))
                    for count2, val in enumerate(final):
                        mast.loc[key, f'Phone {count2}'] = val
                    match = True
                    break
                else:
                    match = False

            if not match:
                maxPhones = len(newPhones)
                newPhoneDict = {}
                for i in range(5):
                    if i > maxPhones - 1:
                        newPhoneDict[i] = 'None'
                    else:
                        newPhoneDict[i] = newPhones[i]

                mast = mast.append({'Name and Business': row['Name'] + ' -- ' + row['Company'],
                                    'ID': 'None',
                                    'Address': 'None',
                                    'Hives': 'None',
                                    'Phone 0': newPhoneDict[0],
                                    'Phone 1': newPhoneDict[1],
                                    'Phone 2': newPhoneDict[2],
                                    'Phone 3': newPhoneDict[3],
                                    'Phone 4': newPhoneDict[4],
                                    'State' : row['State'],
                                    'Notes': row['Description'],
                                    'Email 1': row['Email']
                                    }, ignore_index=True)

    mast.to_excel('new_beekeep_master.xlsx', index=  False)
    mast = master2()

    '''crm input'''
    crm = data['crm input']
    crm = crm[crm['Name'].notna()]
    crm.fillna('None', inplace=True)

    for row in crm.iterrows():
        i, row = row
        if type(row['Phone']) != str:
            continue
        newPhones = []
        for num in row['Phone'].split('//'):
            num = num.replace('-', '').strip()
            num = num.replace('(', '').strip()
            num = num.replace(')', '').strip()
            num = re.sub("[^0-9]", "", num)
            newPhones.append(num)
        newPhones = [p for p in newPhones if p != '']

        for count, ph in enumerate(newPhones):
            for key, ph2 in phones.items():
                if ph in ph2:  # matching phones
                    ph2 = [c for c in ph2 if len(c) > 5]
                    final = list(set(newPhones) | set(ph2))
                    for count2, val in enumerate(final):
                        mast.loc[key, f'Phone {count2}'] = val
                    match = True
                    break
                else:
                    match = False

            if not match:
                maxPhones = len(newPhones)
                newPhoneDict = {}
                for i in range(5):
                    if i > maxPhones - 1:
                        newPhoneDict[i] = 'None'
                    else:
                        newPhoneDict[i] = newPhones[i]

                mast = mast.append({'Name and Business': str(row['Name']) + ' -- ' + str(row['Company Name']),
                                    'ID': 'None',
                                    'Address': row['Address'],
                                    'Hives': 'None',
                                    'Phone 0': newPhoneDict[0],
                                    'Phone 1': newPhoneDict[1],
                                    'Phone 2': newPhoneDict[2],
                                    'Phone 3': newPhoneDict[3],
                                    'Phone 4': newPhoneDict[4],
                                    'State' : row['State'],
                                    'Notes': row['Description'],
                                    'Email 1': row['Email']
                                    }, ignore_index=True)

    mast.to_excel('new_beekeep_master.xlsx', index=  False)

def copy_of_beekeeperz():
    mast = master2()
    data = pd.read_excel('sources/Copy of Beekeeperz.xlsx', sheet_name = None)
    phones = {}
    for row in mast.iterrows():
        i,row = row
        phones[i] = [row[f'Phone {n}'].replace('-', '').strip() for n in range(5)]

    '''new AHPA'''
    ahpa = data['NEW AHPA Members']
    ahpa = ahpa[ahpa['Name'].notna()]
    ahpa.fillna('None', inplace=True)
    for row in ahpa.iterrows():
        i, row = row
        if type(row['Phone #']) != str:
            continue
        newPhones = []
        for num in row['Phone #'].split('//'):
            num = num.lstrip('1-')
            num = num.replace('-', '').strip()
            num = num.replace('(', '').strip()
            num = num.replace(')', '').strip()
            if 'ext' not in num:
                num = re.sub("[^0-9]", "", num)

            newPhones.append(num)
        newPhones = [p for p in newPhones if p != '']

        for count, ph in enumerate(newPhones):
            for key, ph2 in phones.items():
                if ph in ph2:  # matching phones
                    ph2 = [c for c in ph2 if len(c) > 5]
                    final = list(set(newPhones) | set(ph2))
                    for count2, val in enumerate(final):
                        mast.loc[key, f'Phone {count2}'] = val
                    match = True
                    break
                else:
                    match = False

            if not match:
                maxPhones = len(newPhones)
                newPhoneDict = {}
                for i in range(5):
                    if i > maxPhones - 1:
                        newPhoneDict[i] = 'None'
                    else:
                        newPhoneDict[i] = newPhones[i]

                mast = mast.append({'Name and Business': row['Name'] + ' -- ' + row['Business'],
                                    'ID': 'None',
                                    'Address': 'None',
                                    'Hives': 'None',
                                    'Phone 0': newPhoneDict[0],
                                    'Phone 1': newPhoneDict[1],
                                    'Phone 2': newPhoneDict[2],
                                    'Phone 3': newPhoneDict[3],
                                    'Phone 4': newPhoneDict[4],
                                    'Notes': 'None',
                                    'State': row['State'],
                                    'Email 1': row['Email']
                                    }, ignore_index=True)

    mast.to_excel('new_beekeep_master.xlsx', index=  False)
    mast = master2()


    '''beekeeper associtions (micah leads)'''
    micah = data['Micah Leads']
    micah = micah[micah['Name'].notna()]
    micah.fillna('None', inplace=True)
    for row in micah.iterrows():
        i, row = row
        if type(row['Phone # ']) != str:
            continue
        newPhones = []
        for num in row['Phone # '].split('//'):
            num = num.lstrip('1-')
            num = num.replace('-', '').strip()
            num = num.replace('(', '').strip()
            num = num.replace(')', '').strip()
            if 'ext' not in num:
                num = re.sub("[^0-9]", "", num)

            newPhones.append(num)
        newPhones = [p for p in newPhones if p != '']

        for count, ph in enumerate(newPhones):
            for key, ph2 in phones.items():
                if ph in ph2:  # matching phones
                    ph2 = [c for c in ph2 if len(c) > 5]
                    final = list(set(newPhones) | set(ph2))
                    for count2, val in enumerate(final):
                        mast.loc[key, f'Phone {count2}'] = val
                    match = True
                    break
                else:
                    match = False

            if not match:
                maxPhones = len(newPhones)
                newPhoneDict = {}
                for i in range(5):
                    if i > maxPhones - 1:
                        newPhoneDict[i] = 'None'
                    else:
                        newPhoneDict[i] = newPhones[i]

                mast = mast.append({'Name and Business': row['Name'] + ' -- ' + row['Company'],
                                    'ID': 'None',
                                    'Address': 'None',
                                    'Hives': 'None',
                                    'Phone 0': newPhoneDict[0],
                                    'Phone 1': newPhoneDict[1],
                                    'Phone 2': newPhoneDict[2],
                                    'Phone 3': newPhoneDict[3],
                                    'Phone 4': newPhoneDict[4],
                                    'Notes': 'None',
                                    'State': 'None',
                                    'Email 1': row['Email']
                                    }, ignore_index=True)

    mast.to_excel('new_beekeep_master.xlsx', index=  False)
    mast = master2()

    '''colm leads'''
    colm = data['Colm Leads']
    colm = colm[colm['Name'].notna()]
    colm.fillna('None', inplace=True)
    for row in colm.iterrows():
        i, row = row
        if type(row['Phone # ']) != str:
            continue
        newPhones = []
        for num in row['Phone # '].split('//'):
            num = num.lstrip('1-')
            num = num.replace('-', '').strip()
            num = num.replace('(', '').strip()
            num = num.replace(')', '').strip()
            if 'ext' not in num:
                num = re.sub("[^0-9]", "", num)

            newPhones.append(num)
        newPhones = [p for p in newPhones if p != '']

        for count, ph in enumerate(newPhones):
            for key, ph2 in phones.items():
                if ph in ph2:  # matching phones
                    ph2 = [c for c in ph2 if len(c) > 5]
                    final = list(set(newPhones) | set(ph2))
                    for count2, val in enumerate(final):
                        mast.loc[key, f'Phone {count2}'] = val
                    match = True
                    break
                else:
                    match = False

            if not match:
                maxPhones = len(newPhones)
                newPhoneDict = {}
                for i in range(5):
                    if i > maxPhones - 1:
                        newPhoneDict[i] = 'None'
                    else:
                        newPhoneDict[i] = newPhones[i]

                mast = mast.append({'Name and Business': row['Name'] + ' -- ' + row['Company'],
                                    'ID': 'None',
                                    'Address': 'None',
                                    'Hives': 'Q Available',
                                    'Phone 0': newPhoneDict[0],
                                    'Phone 1': newPhoneDict[1],
                                    'Phone 2': newPhoneDict[2],
                                    'Phone 3': newPhoneDict[3],
                                    'Phone 4': newPhoneDict[4],
                                    'Notes': row['Notes'],
                                    'State': 'None',
                                    'Email 1': row['Email']
                                    }, ignore_index=True)

    mast.to_excel('new_beekeep_master.xlsx', index=  False)



def CRM_leads():
    mast = master2()
    data = pd.read_excel('sources/CRM Leads.xlsx')

    data = data[data['Industry'] == 'Beekeeper']
    data.fillna('None', inplace =True)
    data.reset_index(inplace = True)
    names = []
    for i in range(len(data['FirstName'])):
        names.append(str(data['FirstName'][i]) + ' ' + str(data['LastName'][i]))
    data['Name'] = names

    data.drop('FirstName', axis =1, inplace = True)
    data.drop('LastName', axis =1, inplace = True)
    phones = {}
    for row in mast.iterrows():
        i, row = row
        phones[i] = [row[f'Phone {n}'].replace('-', '').strip() for n in range(5)]

    for row in data.iterrows():
        i, row = row

        newPhones = []

        for num in [row['Phone'], row['altPhone'], row['cellPhone'], row['faxPhone']]:
            num = str(num)
            num = num.lstrip('1-')
            num = num.replace('-', '').strip()
            num = num.replace('(', '').strip()
            num = num.replace(')', '').strip()
            if 'ext' not in num:
                num = re.sub("[^0-9]", "", num)

            newPhones.append(num)
        newPhones = [p for p in newPhones if p != '']

        address = str(row['Street']) + ', ' + str(row['City']) + ' ' + str(row['State']) + ' ' + str(row['PostalCode'])
        for count, ph in enumerate(newPhones):
            for key, ph2 in phones.items():
                if ph in ph2:  # matching phones
                    if mast.loc[key, 'Address'] == 'None':
                        mast.loc[key, 'Address'] = address
                    ph2 = [c for c in ph2 if len(c) > 5]
                    final = list(set(newPhones) | set(ph2))
                    for count2, val in enumerate(final):
                        mast.loc[key, f'Phone {count2}'] = val
                    match = True
                    break
                else:
                    match = False

            if not match:
                maxPhones = len(newPhones)
                newPhoneDict = {}
                for i in range(5):
                    if i > maxPhones - 1:
                        newPhoneDict[i] = 'None'
                    else:
                        newPhoneDict[i] = newPhones[i]
                mast = mast.append({'Name and Business': row['Name'] + ' -- ' + row['Company'],
                                    'ID': 'None',
                                    'Address': address,
                                    'Hives': 'None',
                                    'Phone 0': newPhoneDict[0],
                                    'Phone 1': newPhoneDict[1],
                                    'Phone 2': newPhoneDict[2],
                                    'Phone 3': newPhoneDict[3],
                                    'Phone 4': newPhoneDict[4],
                                    'Notes': row['Description'],
                                    'State': row['State'],
                                    'Email 1': row['Email']
                                    }, ignore_index=True)

    mast.to_excel('new_beekeep_master.xlsx', index=  False)


def greg_leads():
    mast = master2()
    data = pd.read_excel('sources/Gregs Leads.xlsx')
    data.fillna('None', inplace =True)
    data.reset_index(inplace = True)
    phones = {}
    for row in mast.iterrows():
        i, row = row
        phones[i] = [row[f'Phone {n}'].replace('-', '').strip() for n in range(5)]

    for row in data.iterrows():
        i, row = row
        if type(row['Phone # ']) != str:
            continue
        newPhones = []
        for num in row['Phone # '].split('//'):
            num = str(num)
            num = num.lstrip('1-')
            num = num.replace('-', '').strip()
            num = num.replace('(', '').strip()
            num = num.replace(')', '').strip()
            if 'ext' not in num:
                num = re.sub("[^0-9]", "", num)

            newPhones.append(num)
        newPhones = [p for p in newPhones if p != '']
        for count, ph in enumerate(newPhones):
            for key, ph2 in phones.items():
                if ph in ph2:  # matching phones
                    ph2 = [c for c in ph2 if len(c) > 5]
                    final = list(set(newPhones) | set(ph2))
                    for count2, val in enumerate(final):
                        mast.loc[key, f'Phone {count2}'] = val
                    match = True
                    break
                else:
                    match = False

            if not match:
                maxPhones = len(newPhones)
                newPhoneDict = {}
                for i in range(5):
                    if i > maxPhones - 1:
                        newPhoneDict[i] = 'None'
                    else:
                        newPhoneDict[i] = newPhones[i]
                mast = mast.append({'Name and Business': row['Name']+ ' -- ' + row['Business'],
                                    'ID': 'None',
                                    'Address': 'None',
                                    'Hives': row['Q Avaliable '],
                                    'Phone 0': newPhoneDict[0],
                                    'Phone 1': newPhoneDict[1],
                                    'Phone 2': newPhoneDict[2],
                                    'Phone 3': newPhoneDict[3],
                                    'Phone 4': newPhoneDict[4],
                                    'Notes': row['Notes'],
                                    'State': 'None',
                                    'Email 1': row['Email ']
                                    }, ignore_index=True)

    mast.to_excel('new_beekeep_master.xlsx', index=  False)


def pollinator():
    mast = master2()
    data = pd.read_excel('sources/pollinator.com.xlsx', sheet_name=None)
    phones = {}
    for row in mast.iterrows():
        i, row = row
        phones[i] = [row[f'Phone {n}'].replace('-', '').strip() for n in range(5)]

    '''new AHPA'''
    for sheet in data.keys():
        currDat = data[sheet]
        currDat = currDat[currDat['NAME'].notna()]
        currDat.fillna('None', inplace=True)
        for row in currDat.iterrows():
            i, row = row
            if 'CITY' not in currDat.columns:
                address = row['ADDRESS']
            else:
                address = str(row['ADDRESS']) + ', ' + str(row['CITY']) + ' ' + str(row['STATE']) + ' ' + str(row['ZIP'])
            newPhones = []
            for num in [row['NUMBER'], row['CELL']]:
                num = num.lstrip('1-')
                num = num.replace('-', '').strip()
                num = num.replace('(', '').strip()
                num = num.replace(')', '').strip()
                if 'ext' not in num:
                    num = re.sub("[^0-9]", "", num)

                newPhones.append(num)
            newPhones = [p for p in newPhones if p != '']

            for count, ph in enumerate(newPhones):
                for key, ph2 in phones.items():
                    if ph in ph2:  # matching phones
                        if mast.loc[key, 'Address'] == 'None':
                            mast.loc[key, 'Address'] = address
                        ph2 = [c for c in ph2 if len(c) > 5]
                        final = list(set(newPhones) | set(ph2))
                        for count2, val in enumerate(final):
                            mast.loc[key, f'Phone {count2}'] = val
                        match = True
                        break
                    else:
                        match = False

                if not match:
                    maxPhones = len(newPhones)
                    newPhoneDict = {}
                    for i in range(5):
                        if i > maxPhones - 1:
                            newPhoneDict[i] = 'None'
                        else:
                            newPhoneDict[i] = newPhones[i]

                    mast = mast.append({'Name and Business': row['NAME'],
                                        'ID': 'None',
                                        'Address':  address,
                                        'Hives': 'None',
                                        'Phone 0': newPhoneDict[0],
                                        'Phone 1': newPhoneDict[1],
                                        'Phone 2': newPhoneDict[2],
                                        'Phone 3': newPhoneDict[3],
                                        'Phone 4': newPhoneDict[4],
                                        'Notes': 'None',
                                        'State': sheet,
                                        'Email 1': 'None'
                                        }, ignore_index=True)
        print(sheet, ' done')
        mast.to_excel('new_beekeep_master.xlsx', index=False)
        mast = master2()


def postprocessing():
    mast = master2()
    ratios = {}
    print(mast[mast['State'] == 'FL'])
    for i, name in enumerate(mast['Name and Business']):
        try:
            nam, bus = [c.strip() for c in name.split('--')]
        except:
            pass
        for name2 in mast['Name and Business']:
            try:
                nam2, bus2 = [c.strip() for c in name2.split('--')]
                ratios[i] = [SequenceMatcher(nam, nam2).ratio(),
                              SequenceMatcher(nam, bus2).ratio(),
                              SequenceMatcher(nam2, bus).ratio(),
                              SequenceMatcher(bus, bus2).ratio()
                              ]
            except:
                pass

    for ind, set in ratios.items():
        if max(set) > .9:
            print(set)



postprocessing()