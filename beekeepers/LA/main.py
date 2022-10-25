import tabula
import sys,os,time
import pandas as pd
import numpy as np
import PyPDF2
import re

def get_text(filepath):
    # creating a pdf file object
    pdfFileObj = open(filepath, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageDict = {}
    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        pageDict[i] = pageObj.extractText()
    pdfFileObj.close()
    return pageDict


def main():
    allText = get_text('LA_beekeeps.pdf')
    contacts = pd.DataFrame(columns=['name', 'phone'])
    counter = 0

    for page in allText.keys():
        currText=allText[page]
        for line in currText.split('\n'):
            if 'registered' in line.lower():
                continue
            if len(re.sub('[^0-9]', '', line))<5:
                name = line.strip().strip('21')
            else:
                phone = line.strip()
                contacts = contacts.append({'name':name,
                                            'phone':phone}, ignore_index=True)
                name = ''
                phone = ''

        contacts.to_excel('LA_contact_list.xlsx',index=False)



if __name__ == '__main__':
    main()