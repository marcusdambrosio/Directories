import tabula



def read_pdf(filepath):
    for p in range(1,10):
        df = tabula.read_pdf(filepath, pages = p)[0]
        print(df.columns)

read_pdf('beekeeper_pdf.pdf')
