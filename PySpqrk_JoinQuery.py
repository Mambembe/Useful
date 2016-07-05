# -*- coding: utf-8 -*-

'''
    - Read csv file
    - Delete useless columns
    - Saves the result in a folder with different test files
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
'''
You have to choose
    - Name of the table you want to load (requires cvs extension)
    - Name of the folder where you want your new csv (it will return an error if the folder already exists)
'''
table_name1 = 'dbo.shop.header_test.dropped'
table_name2 = 'dbo.shop.STAT_storico_dett_test.dropped'
query_folder1 = 'query_Card'
query_folder2 = 'query_Storico'
# --------------------------------------------------------------------


sc = pyspark.SparkContext()
sqlContext = SQLContext(sc)

def CreateTable(table_name, query_folder, output_table):
    path = '/home/matteo/Desktop/BasicNet/SanityCheck/Data/Clean/' + table_name + '.csv'

    table = sc.textFile(path).cache()

    # Divides Header from Table
    temp = table.first()
    table = table.filter(lambda x:x != temp)
    header = temp.split(',')

    def extract(line):
        return [line[i] for i in range(0,len(header))]

    # Deletes all rows whose column-length doesn't match requirements
    data_extract = table.map(lambda line: (line.split(','))) \
        .filter(lambda line: len(line) == len(header)) \
        .map(extract) \
        .cache()

    # --------------- Creates Relational database ----------------------------


    myRow = Row(*header)
    table = data_extract.map(lambda p: myRow(*p))
    interactions_df = sqlContext.createDataFrame(table)
    interactions_df.registerTempTable(output_table)





table1 = CreateTable(table_name1, query_folder1, "table_header")
table2 = CreateTable(table_name2, query_folder2, "table_storico")

prova = sqlContext.sql("""
    SELECT DISTINCT table_header.Flusso FROM table_header,table_storico WHERE table_header.IdOrdine=table_storico.IdOrdine
""")

prova = sqlContext.sql("""
    SELECT IdOrdine FROM table_storico
""")
