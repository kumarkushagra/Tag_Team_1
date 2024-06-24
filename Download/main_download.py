# REMEMBER THAT ZIP_FILE_Path MUST BE EMPTY!!!
# Logic here first deletes all zip files from the directory,then starts DOWNLOADING


from get_all_studies import get_all_studies
from download_study_zip import download_study_zip
from extract_delete_all_zip import Extract_Delete_all_zips
from zip_dir import zip_directory
from delete_all_except_zip import delete_except_zips

def download_studies(downalod_dir,Name_of_ZIP_File, studies = None):
    if studies == None:
        studies = get_all_studies()


    for study_id in studies:
        # Downloading .ziped studies
        download_study_zip(study_id,downalod_dir)
        Extract_Delete_all_zips(downalod_dir)
    zip_directory(downalod_dir,Name_of_ZIP_File)
    delete_except_zips(downalod_dir)




if __name__== "__main__":
    download_dir = "ZIP_FILES"  # Replace with your desired download directory
    # This is an array!!!!!!!!!!!!
    study_id = "fc357979-e1b04273-e83fd9fe-db997ff0-8b9ca1fa"  # Replace with the actual study ID 
    Name_of_ZIP_File="Zip file name"
    download_studies(download_dir,Name_of_ZIP_File)
