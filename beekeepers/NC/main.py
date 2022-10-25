import sys

import tabula

def read_pdf(filepath):
    for p in range(1,10):
        df = tabula.read_pdf(filepath, pages = p)[0]
        cols = ['Company', 'Address', 'City', 'State', 'Zip', 'Phone']
        comp, add,city,state,zip,phone = df.columns
        df.columns=cols
        df = df.append({'Company':comp,
                        'Address':add,
                        'City':city,
                        'State':state,
                        'Zip':zip,
                        'Phone':phone}, ignore_index=True)

        print(df)
        return df

d=read_pdf('nctable.pdf')
d.to_csv('nc_beekeepers.csv', index=False)

