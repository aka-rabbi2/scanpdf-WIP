import os
import pandas as pd 
from PyPDF2 import PdfFileReader
from headers_temp.predict_table import detect_tables
import re
from headers_temp.models import Header 
from scanpdf.models import PdfHeader

from django.core import serializers
import numpy as np

del_list = ('\n', '(')

class Namespace:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)

def clean_header(header):
    global del_list
    for delimiter in del_list:
        header =  header.partition(delimiter)[0]
        clean_header(header)
    


def scan_headers(header_weight_path, bank_weight_path=''):
    # print(os.getcwd())
    
    base_dir = r'headers_temp/pdfs'
    parent_dirs = [os.path.join(base_dir, folder) for folder in os.listdir(base_dir)]

    # all_df = []
    for parent_dir in parent_dirs:
        # print(parent_dir)

        if "jbl" in parent_dir:
            row_tol = 10
        else:
            row_tol = 10
        
        headers = Header.objects.filter(bank = os.path.basename(parent_dir))
        headers_list = serializers.serialize('json', headers)

        files = os.listdir(parent_dir)
        for file in files:
            pdf_path = os.path.join(parent_dir,file)
            args = Namespace(pdf_path=pdf_path, page=0, weights=header_weight_path)

            args2 = Namespace(pdf_path=pdf_path, page=0, weights=bank_weight_path)     

            if file.endswith('.pdf'):

                filename = file.split('.')[0]

                if filename in files:
                        print(filename, ' already exists, skipping')
                        continue

                with open(os.path.join(parent_dir, file),'rb') as f:
                    pdf = PdfFileReader(f)
                    pages = pdf.getNumPages()

                pdf_header = PdfHeader(pdf_name=file)
                for page in range(1,pages+1):
                    args.page = page

                    # row tol decided how many rows are collapsed together
                    df = detect_tables(args, row_tol=row_tol)
                    # df2 = detect_tables(args2, row_tol=row_tol)
                    # print(df2)

                    data = df[0]
                    data.dropna(thresh=3, inplace=True)
                    
                    for i,row in data.iterrows():
                        for idx,bl in enumerate(row.str.match('[a-zA-Z]+')):
                            
                            if not np.isnan(bl):
                                print('aaa', idx, row[idx])
                                header_chunk = re.search(r"^\w+|$", row[idx]).group()
                                pattern = r"\w+(?=\":[\s][\S]{})".format( header_chunk ) # remove anything after newline character

                                result = re.search(pattern, headers_list)
                                print(pattern, result, headers_list)
                                if result:
                                    header = result.group(0)+"_index"
                                    if getattr( pdf_header, header ) == -2021:
                                        setattr(pdf_header, header, idx)
                                    # print(getattr(pdf_header, header))seta
                    pdf_header.save()
                    break

                os.rename(pdf_path,  f"scanpdf/pdfs/{os.path.basename(parent_dir)}/{os.path.basename(pdf_path)}")
