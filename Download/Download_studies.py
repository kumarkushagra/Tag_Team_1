import pandas as pd
import zipfile
import os
import requests
import shutil

def Extract_Delete_all_zips(directory):
    """
    Extracts all ZIP files in the specified directory and deletes the original ZIP files.
    
    Args:
    - directory (str): Path to the directory containing ZIP files.
    
    Returns:
    - None
    """
    # Ensure the directory path ends with a slash for joining correctly
    if not directory.endswith('/'):
        directory += '/'
    
    # Get a list of all files in the directory
    files = os.listdir(directory)
    
    # Iterate through all files
    for file in files:
        if file.endswith('.zip'):
            # Construct the full file path
            file_path = os.path.join(directory, file)
            
            # Extract the contents of the ZIP file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(directory)
            
            # Delete the original ZIP file after extraction
            os.remove(file_path)
            print(f"Extracted and deleted: {file_path}")

def zip_directory(directory_path, zip_path):
    """
    Compresses the folders inside a given directory into a ZIP file.

    Args:
    - directory_path (str): Path to the directory containing folders to be zipped.
    - zip_path (str): Path to the output ZIP file.

    Raises:
    - FileNotFoundError: If the specified directory does not exist.
    """
    # Check if the directory exists
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"The directory '{directory_path}' does not exist.")

    # Initialize the ZIP file object
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through all the items in the directory
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            # Check if the item is a directory
            if os.path.isdir(item_path):
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        # Construct the full local file path
                        local_file = os.path.join(root, file)
                        # Construct the archive path (relative to the directory)
                        archive_name = os.path.relpath(local_file, directory_path)
                        # Add file to ZIP
                        zipf.write(local_file, archive_name)

    print(f"Folders in '{directory_path}' zipped successfully to '{zip_path}'.")

def delete_except_zips(directory):
    """
    Deletes everything inside the specified directory except for .zip files.
    
    Args:
    - directory (str): Path to the directory to clean up.
    
    Returns:
    - None
    """
    # Ensure the directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"The directory '{directory}' does not exist.")

    # Iterate through all files and subdirectories in the directory
    for root, dirs, files in os.walk(directory, topdown=False):
        # Delete subdirectories
        for name in dirs:
            shutil.rmtree(os.path.join(root, name))
        
        # Delete files except for .zip files
        for name in files:
            if not name.endswith('.zip'):
                os.remove(os.path.join(root, name))

def rename_directory(directory_path, new_name):
    """
    Renames a given directory to a new name.
    
    Parameters:
    directory_path (str): The current path to the directory.
    new_name (str): The new name for the directory.
    
    Returns:
    str: The new path to the renamed directory.
    """
    try:
        new_directory_path = os.path.join(os.path.dirname(directory_path), new_name)
        os.rename(directory_path, new_directory_path)
        return new_directory_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_subdirectories(directory):
    """
    Retrieves names of all subdirectories in the given directory.

    Args:
    - directory (str): Path to the directory whose subdirectories are to be listed.

    Returns:
    - list: List containing names of all subdirectories.
    """
    subdirectories = []
    # Get list of all files and directories in the given directory
    contents = os.listdir(directory)
    
    # Iterate through all contents
    for item in contents:
        # Check if the item is a directory
        if os.path.isdir(os.path.join(directory, item)):
            subdirectories.append(item)
    
    return subdirectories


def download_all_studies(download_directory,csv_path ,zip_path, orthanc_url="http://localhost:8042"):
    # Ensure the download directory exists
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    # Get the list of all studies
    studies_url = f"{orthanc_url}/studies"
    response = requests.get(studies_url)
    if response.status_code != 200:
        print("Failed to retrieve studies")
        return
    
    studies = response.json()
    counter = 0
    # Download each study
    for study_id in studies:
        # Store names of old Sub-dir in this array
        old_dir = get_subdirectories(download_directory)
        print(old_dir)

        study_zip_url = f"{orthanc_url}/studies/{study_id}/archive"
        response = requests.get(study_zip_url)
        if response.status_code != 200:
            print(f"Failed to download study {study_id}")
            continue
        
        # Save the study to the download directory
        study_file_path = os.path.join(download_directory, f"{study_id}.zip")
        with open(study_file_path, 'wb') as study_file:
            study_file.write(response.content)
        

        print(f"Downloaded study {study_id} to {study_file_path}")

        # Extract and delete the ZIP files
        Extract_Delete_all_zips(download_directory)
        New_dirs=get_subdirectories(download_directory)
        print(New_dirs)

        new_sub_dir = ""
        new_sub_dir = next(
            (sub_dir for sub_dir in New_dirs if sub_dir not in old_dir),
            None
        )
        print(new_sub_dir)
        # Construct the path of the New Downloadede Directory
        dir_path = download_directory + "/" +  new_sub_dir
        dir_path = os.path.join(download_directory, new_sub_dir)
        dir_path = dir_path.replace("\\", "/") 

        # Fetch the new name the must be assigned
        # file = pd.read_csv(csv_path)
        name = "Normal" + str(counter)
        counter+=1

        # Rename from here
        rename_directory(dir_path,name)



        

    # Zip the directory
    zip_directory(download_directory, zip_path)

    # Delete the extracted sub-directories
    delete_except_zips(download_directory)

# Example usage
if __name__ == "__main__":
    csv_path = "PAth to CSV"
    download_dir = "C:/Users/EIOT/Desktop/Downloads"
    # Define the zip path where the final zip file will be saved
    zip_path = os.path.join(download_dir, "Name_of_ZIP_File.zip")
    # Call the download_all_studies function
    download_all_studies(download_dir,csv_path ,zip_path)