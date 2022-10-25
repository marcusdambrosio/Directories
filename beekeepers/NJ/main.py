import tabula



def read_pdf(filepath):
    for p in range(1,10):
        df = tabula.read_pdf(filepath, pages = p)[0]
        df.columns = df.iloc[0,:]
        df=df.iloc[1:,:]
        print(type(df))
        return df

d=read_pdf('njtable.pdf')
d.to_csv('nj_beekeepers.csv', index=False)

