import PyPDF2

file = open('badPDF.pdf', 'rb')
reader = PyPDF2.PdfFileReader(file)

page = reader.getPage(3)
print(page.extractText())
print(page)