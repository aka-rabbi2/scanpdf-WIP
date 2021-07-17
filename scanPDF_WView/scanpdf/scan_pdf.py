import numpy as np
from datetime import datetime,date
# import pymysql
import os
import pandas as pd 
from PyPDF2 import PdfFileReader
from scanpdf.predict_table import detect_tables
import re
from scanpdf.models import PdfHeader
from showpdf.models import BankInfo, PdfTables
from math import floor

# date_index = None
# particular_index = None
# indexes = []

import traceback


class Namespace:
    def __init__(self,**kwargs):
        self.__dict__.update(kwargs)

class ColumnSpecifier:
    def __init__(self, bank):
        self.bank = bank

    unique_column_name = {
        'bcbl': ['Sr. No','Date','Particulars','Debit\nAmount','Credit\nAmount','Balanced\nAmount'],
        'ibbl': ['Trans Date','Trans Date','Particulars','Withdraw','Deposit','Balance'],
        'ific': ['SL.','Date','Details','Debit','Credit','Balance'],
        'jbl': ['Value Date','Date','Particular','Withdrawal(Dr)','Deposit(Cr)','Balance'],
        'pbl': ['Narration','Date','Narration','Debit','Credit','Balance'],
        'sbac': ['Value Date','Date','Particular','Withdrawal(Dr)','Deposit(Cr)','Balance'],
        'sbl': ['SL','Date','Remarks','Debit Amount','Credit Amount','Balance'],
        'sibl': ['Code','Date','Particulars','Debit','Credit','Balance'],
        'sjibl': ['Narration','Date','Narration','Debit','Credit','Balance'],
        'ubl': ['Trans. Type','Trans. Date','Description','Debit','Credit','Balance'],
    }

    def get_columns(self):
        return self.unique_column_name[self.bank]


def isDate(data):
    
    if len(data.split('/')[-1]) == 2:
        index = data.rfind('/')
        data = data[:index+1]+'20'+data[index+1:]
    for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%d-%b-%Y'):
        try:

            if isinstance(datetime.strptime(data, fmt), date):
                return True, datetime.strptime(data, fmt).strftime('%d/%m/%Y') 
            else:
                return False, None
        except ValueError as e:
            pass
    return False, None
    
def clean_data(df, bank, pdf_name):
    
    data = df[0]

    # data.dropna(thresh=floor(data.shape[1]*0.5), axis=0, inplace=True)
    # data.dropna(thresh=floor(data.shape[0]*0.3),axis=1, inplace=True)
    
    # data = data.T.reset_index(drop=True).T
    data.to_excel(r'temp.xlsx')
    particulars_text = ''
    to_drop = []

    is_particular = False

    # columns = ColumnSpecifier(bank).get_columns()
    header_indexes = PdfHeader.objects.get(pdf_name=pdf_name)

    if header_indexes:
        pass

    index_list = ['dates_index','particulars_index', 'instrument_index', 'withdraw_index', 'deposit_index', 'balance_index']
    
    for idx,row in data.iterrows():
        a = list(row) 
        
        try:
            
            is_date, statement_date = isDate(str(row[header_indexes.dates_index]))
            if not is_date:
                # print(str(row[header_indexes.dates_index]), is_date, statement_date)
                if not row.loc[header_indexes.particulars_index]=='' and is_particular:
                    particulars_text += str(row.loc[header_indexes.particulars_index])
                to_drop.append(idx)
            else:
                # print(str(row[header_indexes.dates_index]), is_date, statement_date)
                # data[idx, header_indexes.dates_index ] = statement_date

                

                data.loc[idx,0] = statement_date 

                # temp_particular_text = data.loc[last_data_idx][header_indexes.particulars_index] 
                                      # changing date format
                if particulars_text != '':
                    
                    # print(type(particulars_text),particulars_text, type(data.iloc[last_data_idx][header_indexes.particulars_index]), temp_particular_text)
                    data.loc[last_data_idx, header_indexes.particulars_index] += particulars_text
                    particulars_text = ''

                is_particular = True
                last_data_idx = idx
                
        except KeyError as e:
            print(e,': searching for heading row...')
        except NameError as e:
            print(e,': searching for heading row...')
        except TypeError as e:
            # print(e)
            print(traceback.format_exc())
            is_particular = True
            last_data_idx = idx


    if particulars_text != '':

        temp_particular_text = data.loc[last_data_idx][header_indexes.particulars_index]
        try:
            if np.isnan(temp_particular_text):
                data.loc[last_data_idx][header_indexes.particulars_index] = particulars_text
        except TypeError:
            print(temp_particular_text, particulars_text)
            data.loc[last_data_idx][header_indexes.particulars_index] += particulars_text

    data.drop(to_drop, inplace=True)
    
    # df_to_insert = data.iloc[:,indexes]
    for index_name in index_list:
        index = getattr(header_indexes, index_name)

        if index == -2021:
            
            globals()[ index_name.split('_')[0] ] = data.iloc[:,0]*0
        else:
            # data.to_excel(r'temp.xlsx')
            globals()[ index_name.split('_')[0] ] = data.loc[:,index]  # globals() 

    # dates = data.iloc[:,header_indexes.dates_index]
    # particulars = data.iloc[:,header_indexes.particulars_index]
    df_to_insert = pd.concat([dates, particulars, instrument, withdraw, deposit, balance], axis=1, ignore_index=True) 

    #df_to_insert = df_to_insert[0:]  #not important

    # df_to_insert.insert(loc=2,column="",value=np.nan)
    
    # df_to_insert = df_to_insert.where(pd.notnull(df_to_insert), None)
    # print(df_to_insert)
    return df_to_insert

def update_data(cleaned_data, bank=''):
    if not cleaned_data.empty and bank:

        for _,row in cleaned_data.copy().iterrows():
            bank_object = BankInfo.objects.create(shorthand=bank)
            bank_object.save()
            for fmt in ('%d/%m/%Y', '%d-%m-%Y'):
                try:
                    row[0] =  datetime.strptime(row[0], fmt)
                    data_iter = iter(row)
                    datapoints = PdfTables(
                        bank=bank_object, date=data_iter.__next__(), particulars=data_iter.__next__(), instrument=data_iter.__next__(),
                        withdraw=data_iter.__next__(), deposit=data_iter.__next__(), balance=data_iter.__next__() )

                    datapoints.save()
                    break
                except ValueError as e:
                    # print(e)
                    print(traceback.format_exc())
                except TypeError as e:
                    # print(e)
                    print(traceback.format_exc())

        del cleaned_data
        
        

        # del cleaned_data    

def scan_pdf(weight_path):

    base_dir = r'scanpdf/pdfs'
    parent_dirs = [os.path.join(base_dir, folder) for folder in os.listdir(base_dir)]
    # all_df = []
    for parent_dir in parent_dirs:
        # print(parent_dir)



        if "jbl" in parent_dir:
            row_tol = 10
        else:
            row_tol = 10
        files = os.listdir(parent_dir)
        for file in files:
            pdf_path = os.path.join(parent_dir,file)
            args = Namespace(pdf_path=pdf_path, page=0, weights=weight_path)           
            if file.endswith('.pdf'):

                filename = file.split('.')[0]

                if filename in files:
                        print(filename, ' already exists, skipping')
                        continue

                with open(os.path.join(parent_dir, file),'rb') as f:
                    pdf = PdfFileReader(f)
                    pages = pdf.getNumPages()


                for page in range(1,pages+1):
                    args.page = page

                    # row tol decided how many rows are collapsed together
                    df = detect_tables(args, row_tol=row_tol)
                    
                    try:
                        cleaned_data = clean_data(df, os.path.basename(parent_dir), file)

                        update_data(cleaned_data, os.path.basename(parent_dir))
                    except Exception as e:
                        # print(e)
                        print(traceback.format_exc())

            # os.rename(pdf_path,  f"scanpdf/scanned/{os.path.basename(pdf_path)}")