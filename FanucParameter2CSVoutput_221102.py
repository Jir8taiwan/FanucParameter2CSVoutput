#!/usr/bin/python3
#vim:fileencoding=utf-8
import pandas as pd
import update
import csv
import os, sys
import openpyxl
import time
#from tqdm import tqdm
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
#####################
# Author: JIR
# Version. 2022.11.02
#
# Using PYTHON3 language to open and convert at FANUC controller system of parameter backup.
# Please copy "CNC-PARA.TXT" in program folder together.
# It will output CSV and EXCEL files for studying in a formatted data.
#
#####################
print("FanucParameter2CSVoutput by JIR made")
print()
## Configure
TXTinputPATH = 'CNC-PARA.TXT'           #參數檔案
CSVoutputPATH2 = '1_Output.CSV'         #CSV輸出，無篩選。
CSVoutputPATH3 = '2_Output_trimed.CSV'  #CSV輸出，篩選空資料。
XLSXoutputPATH2 = '3_Output.xlsx'       #EXCEL輸出，無篩選。
XLSXoutputPATH = '4_Output_trimed.xlsx' #EXCEL輸出，篩選空資料。

## Compare and calculate 以下計算用
TEMPouputPATH = 'tempoutput.txt'
TEMPouputPATH2 = 'tempoutput2.txt'
CSVoutputPATH = 'OutputTemp.CSV'

## DEF
def filter_rows_by_values(df, col, values):
    return df[~df[col].isin(values)]

## Go Loop
print("Please select the PARAMETER file such as ", TXTinputPATH)
print()
file_path = filedialog.askopenfilename(title = "Select PARAMETER file",filetypes = (("TXT files","*.txt"),("all files","*.*")), initialdir='./')

if str(type(file_path))=="<class 'tuple'>" or file_path == '':
    print("FILE INPUT is going to open default :", TXTinputPATH)
    print()
    TXTinputPATH = TXTinputPATH
else:
    print("FILE INPUT is different than default :", TXTinputPATH)
    print("Anyhow, it uses new select file to go on :", file_path)
    print()
    TXTinputPATH = file_path

## Check defailt CNC-PARA.TXT, if no existed is exit
if not os.path.exists(TXTinputPATH):
    print("Please confirm \"", TXTinputPATH, "\" file that is correct filename or really existed in folder.")
    print()
    time.sleep(5)
    sys.exit(0)

## converting
print("Converting and processing!!")
print()
txt = ""
with open(TXTinputPATH, 'r', encoding='UTF-8') as file:
    #while (line := file.readline().rstrip()):
    nonempty = filter(str.rstrip, file)
    for line in nonempty:
        if "%" in line.strip():
            line = ""
        paramNUM = str(line[:6])
        #paramNUM = line.rsplit('Q1L1P', 1)[0]

        ##### for older bck format
        #line = re.sub(r"\s+", ",", line)
        line = line.replace(" ", "")
        if not len(line) == 0:
            if not line[6:8] == "Q1":
                #print(line[6:8])
                line = line[:6] + "Q1" + line[6:]
        

        ##### for newer bck format                
        #line = line.replace("A11P", "\nA11")
        line = line.rsplit('A7', 1)[0]
        line = line.rsplit('S5', 1)[0]
        
        line = line.replace("Q1L1P", ",L1,")
        line = line.replace("L2P", "\n" + paramNUM + ",L2,")
        line = line.replace("L3P", "\n" + paramNUM + ",L3,")
        line = line.replace("L4P", "\n" + paramNUM + ",L4,")

        line = line.replace("Q1A1M", ",A1,")
        line = line.replace("A2M", "\n" + paramNUM + ",A2,")
        line = line.replace("A3M", "\n" + paramNUM + ",A3,")
        line = line.replace("A4M", "\n" + paramNUM + ",A4,")
        line = line.replace("A5M", "\n" + paramNUM + ",A5,")
        line = line.replace("A6M", "\n" + paramNUM + ",A6,")

        line = line.replace("Q1L1M", ",A1,")
        line = line.replace("L2M", "\n" + paramNUM + ",L2,")
        line = line.replace("L3M", "\n" + paramNUM + ",L3,")
        line = line.replace("L4M", "\n" + paramNUM + ",L4,")

        line = line.replace("Q1T1P", ",T1,")
        ine = line.replace("T2P", "\n" + paramNUM + ",T2,")
        line = line.replace("T3P", "\n" + paramNUM + ",T3,")
        line = line.replace("T4P", "\n" + paramNUM + ",T4,")

        line = line.replace("Q1M", ",M,")
        
        line = line.replace("Q1S1P", ",S1,")
        line = line.replace("S2P", "\n" + paramNUM + ",S2,")
        line = line.replace("S3P", "\n" + paramNUM + ",S3,")
        line = line.replace("S4P", "\n" + paramNUM + ",S4,")
        
        line = line.replace("Q1A1P", ",A1,")
        line = line.replace("A2P", "\n" + paramNUM + ",A2,")
        line = line.replace("A3P", "\n" + paramNUM + ",A3,")
        line = line.replace("A4P", "\n" + paramNUM + ",A4,")        
        line = line.replace("A5P", "\n" + paramNUM + ",A5,")
        line = line.replace("A6P", "\n" + paramNUM + ",A6,")
        line = line.replace("A7P", "\n" + paramNUM + ",A7,")
        line = line.replace("A8P", "\n" + paramNUM + ",A8,")
        line = line.replace("A9P", "\n" + paramNUM + ",A9,")
        line = line.replace("A10P", "\n" + paramNUM + ",A10,")
        line = line.replace("A11P", "\n,A11,")
        line = line.rsplit(',A11', 1)[0]

        line = line.replace("Q1P", ",,")
        #print("Formating:", line)
        txt += line + "\n"
        
f = open(TEMPouputPATH,'w',encoding='utf-8')
#txt = txt.strip()
f.write(txt)
f.close()

file.close()

#print()
#print(txt) 

## Output file
print("Outputing new format CSV file")
print()
f = open(TEMPouputPATH,'w', encoding='utf-8')
txt = txt.strip()
f.write(txt)
f.close()

with open(TEMPouputPATH, 'r', encoding='utf8') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open(CSVoutputPATH, 'w') as out_file:
        writer = csv.writer(out_file, dialect="excel")
        writer.writerow(['ParamNO', 'AxisName', 'Value'])
        writer.writerows(lines)
        out_file.close()


with open(CSVoutputPATH, newline='', encoding='utf8') as in_file:
    with open(CSVoutputPATH2, 'w', newline='') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if row:
                writer.writerow(row)
        out_file.close()
        
# check temp file and exited is to delete
if os.path.exists(CSVoutputPATH):
    os.remove(CSVoutputPATH)

## Make a CSV format file without 0 value of data
print("Outputing CSV file without 0 value data")
print()
df = pd.read_csv(CSVoutputPATH2, encoding='utf8', dtype=str)
if os.path.exists(CSVoutputPATH3):
    os.remove(CSVoutputPATH3)
new_df = filter_rows_by_values(df, "Value", ["0","00000000", "0.0"])
#print(new_df)
new_df.to_csv(CSVoutputPATH3, index=False, encoding='utf8')

## Make a EXCEL format file with and without 0 value of data
print("Outputing EXCEL file from CSV data")
print()
read_file = pd.read_csv(CSVoutputPATH3, encoding='utf8', dtype=str)
read_file.to_excel(XLSXoutputPATH, index=None, header=True)
read_file = pd.read_csv(CSVoutputPATH2, encoding='utf8', dtype=str)
read_file.to_excel(XLSXoutputPATH2, index=None, header=True)

## Finish to know
print("Conveting is DONE!!")
print()
print("It will close in 5 seconds automatically...")
print()
time.sleep(5)


      
