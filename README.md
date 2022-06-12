# load_csv_files_to_postgres 
# Insert CSV file data into Postgres DB using Python

This repo will give you the tools needed to insert as many csv files as you would like into a Postgres DB. It will create a table using the CSV file name and it will insert the data from the CSV file into the table. 

The script will currently drop the table if one already exists with the same name.

The instructions below assume you already have a Postgres DB set up.

1)Clone this git hub repo using the HTTP method or downloading the Zip file.

2)Once you have cloned the repo you should have 2 files, csv_import_functions.py and import_csv_file.py.
 a) csv_import_functions.py - Contains all the Python functions and set commands, you will need to update this later on.
 b) import_csv_file.py - This is the script which will actually be ran, this script should not need to be udpated.

3)Within the directory where you cloned the repo, open your terminal and run the following commands.
  a) python3 -m venv env = Initialises virtual ENV for this specific folder (You do not have to do this but I like to keep my projects separated)
  b) Use pip to install the following libraries
    aa)pandas, psycopg2, numpy

4)Once that has been completed open the csv_import_functions.py script, you will need to update the following
  a)file_path = This is this file path location where your csv files will be stored.
  b)dataset_dir = This is the file path location where your csv files will be MOVED before loading.
  c)conn_string = This is the connection string for your Postgres environment, in the example I am hosting mine on my LocalPC however you could also use a cloud environment if you wish.

5)Now all that is left to do is run the script. Currently the script only strips out spaces from the file names and the column headers, I will udpate the script later down the line to do more cleaning.
  a)Run script = from your terminal run "python3 import_csv_file.py"

6)If all was successful you should be greeted with the following output commands in your terminal
['test customer.csv']
test_customer
PostgreSQL Drop table if exists....
PostgreSQL Create table if it doesnot exist using SQL query built above....
file opened in memory
file inserted into DB
Table test_customer imported to db completed
all tables have been imported into the db
  a)Within your Postgres DB you should also find a table with the name of your CSV file(s) and the contents from the CSV file should have been loaded into the table.
