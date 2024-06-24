# import requests
from Fetch_UHID import return_uhid_array
from Generate_Full_dir_Path import join_paths
from Generate_Batches_Dir import create_subdirectory
from batch_number import latest_batch_number
from Copy_to_Batch_dir import copy_directories_to_Batch_dir
from Upload_Entire_Batch.Upload_batch import Upload_Batch
import os

from Upload_Entire_Batch.list_UHIDs import list_subdirectories 
from Upload_Entire_Batch.generate_series_path import generate_all_series_path
from Upload_Entire_Batch.update_master_csv import update_csv
from Upload_Entire_Batch.upload_each_series import upload_dicom_files
from Upload_Entire_Batch.anonymize_given_study import anonymize_study
from Upload_Entire_Batch.append_to_mapping_csv import append_to_csv
from Upload_Entire_Batch.delete_study import delete_studies
from Upload_Entire_Batch.rename_studyID import rename_patient




def Upload(unzip_dir,anonymize_flag, target_dir,csv_file_path,batch_size):
    UHIDs = return_uhid_array(csv_file_path, batch_size, "LLM", 0,"Uploaded", 0, "Patient ID (UHID)")
    # print(UHIDs)
    batch_number = latest_batch_number()
    batch_Name = "Batch" + str(batch_number+1)
    # print(batch_Name)
    # create_subdirectory(target_dir,batch_Name)

    Paths_to_copy= join_paths(unzip_dir, UHIDs)
    print(Paths_to_copy)


    # Full path of BATCH0X i.e. just created 
    target_dir ="Contains_Batches/"+  batch_Name 
    if not os.path.exists(target_dir):
        # Create a new directory because it does not exist
        os.makedirs(target_dir)

    # Copying files from Unziped DIR to Batches
    copy_directories_to_Batch_dir(target_dir, Paths_to_copy)


    # Uploading Entire Batch
    Upload_Batch(target_dir, anonymize_flag, csv_file_path,batch_Name)

if __name__=="__main__":
    csv_file_path="C:/Users/EIOT/Desktop/Final.csv"
    batch_size=5
    anonymize_flag= True
    target_dir="Contains_Batches/"
    unzip_dir="C:/Users/EIOT/Desktop/Unziped_dir"
    Upload(unzip_dir,anonymize_flag, target_dir,csv_file_path,batch_size)
