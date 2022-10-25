import sys,os,time
import pandas as pd
import PyPDF2


def read_txt(filepath):
    file = open(filepath,'rb')
    for i in file.readlines():
        print(i)
        time.sleep(1)
read_txt('SD_list.txt')