"""
Script Name: to_label_map
Author: Noor Borren 
Date: 05-07-2023
Description: Needs to be run from the terminal but can be adjusted to run it in the Python interpreter of course.
The script loops over all patients with a CSV-file and needs access to the original NIfTI-file. Then, it takes the
voxel coordinates of the markerpoints to create 3D blobs, corrected for pixel spacing. The label map is then saved
as a new NIfTI file. The numbers corresponding to the pixel values of the blobs correspond to the labels in the 
JSON-files. 
"""

import argparse
import os
import glob 
import pandas as pd 
import numpy as np 
import SimpleITK as sitk 


# Run from command line 
#C:\Users\vmart\miniconda3\python.exe to_label_map.py --CSV "C:\Users\vmart\Documents\TM_jaar_3\Afstuderen\Thesis\labels_csv" --output_dir "C:\Users\vmart\Documents\TM_jaar_3\Afstuderen\Thesis\labels_nifti" --OG "C:\Users\vmart\Documents\TM_jaar_3\Afstuderen\Thesis\NIFTI"


parser = argparse.ArgumentParser(description="Prepares image labels for nnDetection")
parser.add_argument("--OG", dest = "dir_original_image", help="Give the absolute path to the directory of the original images")
parser.add_argument('--CSV', dest = "dir_csv_Mev", help= "Give the absolute path to the directory with the .csv files outputted by MeVisLab")
parser.add_argument('--output_dir', dest = "output_dir")
args = parser.parse_args()

# # Split arguments from command line 
dir_original_img = args.dir_original_image
dir_csv = args.dir_csv_Mev

CSV_files = glob.glob(dir_csv + '\*.csv')
output_dir = args.output_dir

# Set variables
label_mask = 'blob' # set to 'gaussian' for gaussian blobs but not updated! 
sigma = 10
radius = 7


def create_label_mask(img_shape, list_markers, voxel_spacing, radius_blob=radius, label_mask='blob'):
    blobs = np.zeros(img_shape, dtype=np.float32)

    for point in range(len(list_markers[0])):

        marker_coor = (list_markers[0][point], list_markers[1][point], list_markers[2][point])
        x, y, z = np.meshgrid(
            np.arange(max(0, marker_coor[0] - 2*radius_blob), min(img_shape[0], marker_coor[0] + 2*radius_blob)),
            np.arange(max(0, marker_coor[1] - 2*radius_blob), min(img_shape[1], marker_coor[1] + 2*radius_blob)),
            np.arange(max(0, marker_coor[2] - 2* radius_blob), min(img_shape[2], marker_coor[2] + 2*radius_blob)),
            indexing='ij',
            copy=False,
        )
        distance = np.sqrt(((x - marker_coor[0]) * voxel_spacing[0])**2 + ((y - marker_coor[1]) * voxel_spacing[1])**2 + ((z - marker_coor[2]) * voxel_spacing[2])**2)

        if label_mask == 'blob':
            mask = np.array(np.where(distance <= radius_blob))
            xx = mask[0,:] + marker_coor[0].astype(int) - np.mean(mask[0,:]).astype(int)
            yy = mask[1,:] + marker_coor[1].astype(int) - np.mean(mask[0,:]).astype(int)
            zz = mask[2,:] + marker_coor[2].astype(int) - np.mean(mask[0,:]).astype(int)
            blobs[xx, yy, zz] = point + 1
        elif label_mask == 'gaussian': # In later iterations not updated so doesnt work now 
            blob_gaus = np.exp(-((x - marker_coor[0])**2 + (y - marker_coor[1])**2 + (z - marker_coor[2])**2) / (2 * sigma**2))
            blobs[x, y, z] += blob_gaus
    return blobs


def set_img_data(label_mask, original_img):
    
    label_mask_trans = np.transpose(np.array(label_mask), (2, 1, 0)) 
    result_image = sitk.GetImageFromArray(label_mask_trans) 

    # Set the transformation matrix of the label mask to match the original image
    result_image.SetDirection(original_img.GetDirection())
    result_image.SetOrigin(original_img.GetOrigin())
    result_image.SetSpacing(original_img.GetSpacing())
    return result_image 


def data_from_csv(path_string):
    data = pd.read_csv(path_string)

    # Define Image shape of original image 
    img_shape = (data['X_size'][0], data['Y_size'][0], data['Z_size'][0])
    list_markers = [data['vox_x'].values, data['vox_y'].values, data['vox_z'].values]
    return img_shape, list_markers

saved_patients = [os.path.splitext(os.path.basename(file))[0].split('.nii')[0] for file in glob.glob(output_dir + '/*.nii.gz')]

for number, patient in enumerate(CSV_files): 
    # patient is path to CSV file 
    filename = os.path.basename(patient)
    patient_name = filename.split('.')[0]

    # Skip if patient is already saved
    if patient_name in saved_patients:
        print(f'Skipping {patient_name} as it is already saved')
        continue

    original_img = os.path.join(dir_original_img + "/" + patient_name + ".nii.gz") #Path to original image; add _image for RibFrac
    original_image = sitk.ReadImage(original_img)
    vox_spacing = original_image.GetSpacing()

    # Create label mask 
    img_shape, list_markers = data_from_csv(patient) # Obtain important input for next definition
    label_mask = create_label_mask(img_shape, list_markers, vox_spacing, radius_blob=10) 
    transformed_label_mask = set_img_data(label_mask, original_image)

    # Save image to output directory
    sitk.WriteImage(transformed_label_mask, output_dir + '/' + patient_name + '.nii.gz')
    print(f'{patient_name} is saved, done {number+1}/{len(CSV_files)}')
    
    

  




