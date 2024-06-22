# upload_Files(dir_path, CSV_Path, Anon_Flag, Batch_Size, Log_file_name):
    # Target_UHID array = Fetch_Uhid(
    #                               CSV_path,
    #                               Batch_Size,
    #                               column_name1, 
    #                               value1, 
    #                               column_name2,
    #                               value2,
    #                               id_column_name) 
'''
make sure to check 2 columns to shortlist the UHIDs (Uploaded & Status) 
'''
    # Generate Full path (For UHID_Dir) = Generate_Full_Path(Parent_Dir, Uhid_array) 
    # Copy_to_New_Directory(Destination_Path , source_dir_array)
    # Upload_Batches( Path_of_Destination_Path ) Anonymizes, deletes, Records CSV , Mapping


      