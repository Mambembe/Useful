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

SPARK_HOME = '/home/matteo/Spark/'
os.environ['SPARK_HOME'] = os.path.join(SPARK_HOME)
sys.path.append('/home/matteo/Spark/python/')
import pyspark
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql import Row

# --------------------------------------------------------------------
path = '/home/matteo/Desktop/BasicNet/SanityCheck/Data/'
table_name = 'dbo.shop.header'
columnsIndex = [0,1]#range(0,10)
saving = False
# --------------------------------------------------------------------

# Load SparkContext
try:
    sc = pyspark.SparkContext()
    sqlContext = SQLContext(sc)
except:
    print ("Error loading the SparkContext")
    sys.exit(0)

# Load csv
try:
    table = sc.textFile(path + table_name + '.csv').cache()
    rows = int(table.count())
    temp = table.first()
except:
    print ("Errors Loading the csv file")
    sys.exit(0)

# Generates Header
try:
    table = table.filter(lambda x:x != temp)
    header = temp.split(',')
    if (columnsIndex != 0):
        header_final = [header[i] for i in columnsIndex]
    else:
        columnsIndex = range(0,len(header))
        header_final = header
except:
    print ("Errors while generating the header")
    sys.exit(0)

def extract(line):
    a = True
    return bool(a)#[line[i] for i in range(0,len(header))]

def prova(line):
    try:
        lambda line: extract(line)
        return True
    except:
        return False

#.map(extract, columnsIndex) \

# Process csv
try:
    data_extract = table.map(lambda line: (line.split(','))) \
        .filter(prova)\
        .filter(lambda line: len(line) == len(header)) \
        .cache()
    rowsAfter = int(data_extract.count())
except:
    print ("Errors while processing csv")
    sys.exit(0)



try:
    if saving:
        data_extract.saveAsTextFile(path+str(table_name)+'_clean.csv')
except:
    print ("Errors while saving the processed csv")
    sys.exit(0)

try:
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
except:
    print ("Errors while saving test results")
    sys.exit(1)

print "Success!"
