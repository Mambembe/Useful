# -*- coding: utf-8 -*-

'''
INPUT:
    - Table name (without the csv extension)
    - Indexes of columns you do not want to drop
        --> If columnsIndex = 0 then all columns will be saved
    - saving = "true/false"

OUTPUT:
    - Read csv file
    - Delete useless columns
    - Generates a new csv made up of multiple files
    - Returns a txt file with some results from the deleting phase
'''

import sys
import os
import pandas as pd

SPARK_HOME = '/home/matteo/Spark/'
os.environ['SPARK_HOME'] = os.path.join(SPARK_HOME)
sys.path.append('/home/matteo/Spark/python/')
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql import Row



# --------------------------------------------------------------------
table_name = 'VW_STAT_Storico_Articoli'
columnsIndex = 0#range(0,10)
saving = True
# --------------------------------------------------------------------


path = '/home/matteo/Desktop/BasicNet/SanityCheck/Data/'
sc = pyspark.SparkContext()
sqlContext = SQLContext(sc)
table = sc.textFile(path+table_name+'.csv').cache()

# Divides Header from Table
temp = table.first()
table = table.filter(lambda x:x != temp)
header = temp.split(',')

def extract(line, _columnsIndex):
    if (_columnsIndex != 0):
        return [line[i] for i in _columnsIndex]
    else:
        return [line[i] for i in len(header)]

if (columnsIndex != 0):
    header_final = [header[i] for i in columnsIndex]
else:
    header_final = header

data_extract = table.map(lambda line: (line.split(','))) \
    .filter(lambda line: len(line) == len(header)) \
    .map(extract, columnsIndex) \
    .cache()

rows = int(table.count())
rowsAfter = int(data_extract.count())

if saving:
    data_extract.saveAsTextFile(path+str(table_name)+'_clean.csv')


file_name = str(table_name)+'_Results.txt'

f = open(path + file_name, "w")
f.write('----------- Test Results for ' + table_name + ' -----------\n\n')
f.write('Columns : \n%s\n\n' %header)
f.write('Saved columns:\n%s\n\n' %header_final)
f.write('Number of columns before cleaning = %i\n' % len(header) + '\n')
f.write('Number of columns after cleaning = %i\n' % len(header_final) + '\n')
f.write('Number of rows before cleaning = %i' % rows +'\n\n')
f.write('Number of rows after cleaning = %i' % rowsAfter +'\n\n')
f.write('Number of deleted rows = %i' % (rows-rowsAfter))
f.close()