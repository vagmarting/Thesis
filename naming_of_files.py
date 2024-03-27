"""
Script Name: naming_of_files
Description: The script formats the names of the files so it can be used in nnDetection and nnU-Net. See documentation
of the original github / article why this is needed and which files need which naming. 
"""
import os

######## TO FILL ##########
folder_path = r"C:\Users\vmart\Documents\TM_jaar_3\Afstuderen\Thesis\labels_csv"
extension = '.csv'#".csv"
scanner = "0000" # or 0

def reformat_file_names(folderpath, extension, scanner=0):
    # Get a list of all files in the folder
    nifti_files = [file for file in os.listdir(folderpath) if file.endswith(extension)]

    # Rename the files
    for file in nifti_files:
        original_name = os.path.join(folderpath, file)
        if scanner == '0000':
            new_name = os.path.join(folderpath, f"{file[:12]}_0000{extension}")
        else: 
            new_name = os.path.join(folderpath, f"{file[:12]}{extension}")

        if os.path.exists(new_name):
                print(f"Skipping file '{file}' - Target filename already exists: '{new_name}'")
                continue
        try:
            os.rename(original_name, new_name)
            print(f"Renamed '{file}' to '{new_name}'")
        except OSError as e:
            print(f"Error renaming file '{file}': {e}")
            
reformat_file_names(folder_path, extension, scanner)