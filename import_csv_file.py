from csv_import_functions import *

#Main function
csv_files = csv_files()
configure_dataset_directory(csv_files, dataset_dir)
df = create_dataframe(dataset_dir, csv_files)

#main2 functions
for f in csv_files:
    dataframe = df[f]
    tbl_name = clean_tbl_name(f)
    col_str, dataframe_columns = clean_columns(dataframe)
    upload_to_db(tbl_name, col_str, file=f, dataframe=dataframe, dataframe_columns=dataframe.columns)

