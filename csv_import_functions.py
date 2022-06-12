from ast import excepthandler
from distutils.command.upload import upload
import os
import numpy as np
import pandas as pd
import psycopg2

#Find only CSV files in the specifed path below

file_path = ''
#Make a new directory for the csv files so we can move them into there

dataset_dir = ''

#Connection string to connect to the postgres DB
#Example below
conn_string = "postgresql://postgres:password@localhost/dbnmae"

#Get list of all files and save to all_files variable

all_files = os.listdir(file_path)

#create blank list variable so we can add the csv file names to it from the for loop
#for loop to go through all the files found in the test_files dir and add only the ones which have a .csv ext to my csv file list variable

def csv_files():
    csv_files = []
    for file in all_files:          
        if file.endswith('.csv'):    
            csv_files.append(file)
    return csv_files

#create the bash command to make the new dir, pass on any errors as the error will most likely be that the folder already exists 
def configure_dataset_directory(csv_files, dataset_dir):
    try:
        mkdir = 'mkdir {0}'.format(dataset_dir)
        os.system(mkdir)
    except:
        pass

    #move csv files into the new dir 
    for csv in csv_files:
        try:
            move_files = "mv '{0}' {1}".format(file_path + csv, dataset_dir)
            os.system(move_files)
        except:
            pass
    return

#This function will create and return the pandas data frames
def create_dataframe(dataset_dir, csv_files):
    df = {}
    #this is just reading in my csv file and setting it to the a variable called df
    for file in csv_files:
        try:
            df[file] = pd.read_csv(dataset_dir+file)
            print(csv_files)
        except UnicodeDecodeError:
            df[file] = pd.read_csv(dataset_dir+file, encoding="ISO-8859-1")
    return df

#This function takes in a file name and cleans it and removes the ext and returns it
def clean_tbl_name(filename):
    clean_tbl_name = filename.lower().replace(" ","_")
    #Remove .csv file ext from clean_tbl_name varible so that can be used as the table name
    clean_tbl_name_no_ext = '{0}'.format(clean_tbl_name.split('.')[0])
    print(clean_tbl_name_no_ext)
    return clean_tbl_name_no_ext

#this will loop through each column in the data frame and remove any spaces and make everything lower case, return col_str and the dataframe columns
def clean_columns(dataframe):
    dataframe.columns = [x.lower().replace(" ","_") for x in dataframe.columns]
    #create dictionary which will convert the pandas types to sql data types

    replacements = {          
    "object": "varchar",
    "float64": "float",
    "int64": "int"
    }
    col_str = ", ".join("{} {}".format(n, d) for (n, d) in zip(dataframe.columns, dataframe.dtypes.replace(replacements)))
    return col_str, dataframe.columns

def upload_to_db(tbl_name, col_str, file, dataframe, dataframe_columns):    

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    # execute a statement
    # Form the SQL statement - DROP TABLE
    dropTableCommand = 'DROP TABLE IF EXISTS %s;'%tbl_name
    try:
        print('PostgreSQL Drop table if exists....')
        cursor.execute(dropTableCommand)
        conn.commit()
    except Exception as e:
        print(e)

    #Create table if table DOESNT already exist

    try:
        print('PostgreSQL Create table if it doesnot exist using SQL query built above....')
        cursor.execute('create table %s (%s);'%(tbl_name, col_str))
        conn.commit()
    except Exception as e:
        print(e)

    #Save df to csv file
    dataframe.to_csv(file, header=dataframe.columns, index=False, encoding='utf-8')
    
    #open the csv file in memory
    my_file = open(file)
    print('file opened in memory')
    #upload to db
    SQL_STATEMENT = """
    Copy %s FROM STDIN WITH
        CSV
        HEADER
        DELIMITER AS ','
    """
    cursor.copy_expert(sql=SQL_STATEMENT % tbl_name,file=my_file)
    conn.commit()
    print('file inserted into DB')
    
    cursor.execute('grant select on table %s to public'%(tbl_name))
    conn.commit()

    cursor.close()
    print("Table {0} imported to db completed".format(tbl_name))

    #for loop compelted 
    print('all tables have been imported into the db')   
