"""
Description: The script uses the information derived from the CSV-files to format three different JSON-files for the classification of rib fractures. 
"""

import json
import os
import pandas as pd 


# Directory to CSV files from MeVisLab 
csv_dir = r'C:\Users\vmart\Documents\TM_jaar_3\Afstuderen\Thesis\labels_csv'
output_dir_type = r'C:\Users\vmart\Documents\TM_jaar_3\Afstuderen\Thesis\JSON\labels_location'

# # Create an empty dictionary
data_dict = {}

dict_fract_type = {'simple': 0, 'wedge': 1, 'complex': 2}
dict_fract_displacement = {'undisplaced': 0, 'offset': 1, 'displaced': 2}
rib_number = {'L1': 0, 'L2': 1, 'L3': 2, 'L4': 3, 'L5': 4, 'L6': 5, 'L7': 6, 'L8': 7, 'L9': 8, 'L10': 9, 'L11': 10, 'L12': 11,
               'R1': 12, 'R2': 13, 'R3': 14, 'R4': 15, 'R5': 16, 'R6': 17, 'R7': 18, 'R8': 19, 'R9': 20, 'R10': 21, 'R11': 22, 'R12': 23}

swapped_dict = {value: key for key, value in rib_number.items()}


def name_to_number(label):
   if label == 'simple':
     number = 0
   elif label == 'wedge':
     number = 1
   elif label == 'complex':
     number = 2
   return number 

def location_to_number(label):
   if label == 'anterior':
     number = 0
   elif label == 'lateral':
     number = 1
   elif label == 'posterior':
     number = 2
   return number 

def disp_to_number(label):
   if label == 'undisplaced':
     number = 0
   elif label == 'offset':
     number = 1
   elif label == 'displaced':
     number = 2
   return number 

def generate_json_fractype(output_folder: str, file_name: str,
                           instances: dict,
                           ):
#   """ Example instances:
#         {
#             '1': 0, 
#             '2': 1,
#             '3': 1,
#         }
#         These corresponds with the dataset.json where 
#         {
#           'Simple' : 0, 
#           'Wedge'  : 1, 
#           'Complex': 2,
#         }
#         """
   dataset_json = {'instances': instances}
   suffix = '.json'
   path_json = os.path.join(output_folder, file_name + suffix)
   with open(path_json, 'w') as outfile:
     json.dump(dataset_json, outfile)

 # Loop over all csv files in the directory
for file_name in os.listdir(csv_dir):
     if file_name.endswith('.csv'):
         data_dict = {}
         # Load the csv file into a pandas dataframe
         df = pd.read_csv(os.path.join(csv_dir, file_name))
         for i in range(len(df['location'])):
           #data_dict[i+1] = name_to_number(df['type'][i])
           data_dict[i+1] = location_to_number(df['location'][i])
           #data_dict[i+1] = disp_to_number(df['location'][i])
           #data_dict[i+1] = int(df['rib_number'].map(rib_number)[i])
         generate_json_fractype(output_dir_type, file_name[:-4], data_dict)



# # # Get a list of all CSV files in the directory
# csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]

# Iterate over each CSV file and load it into a pandas DataFrame
# for csv_file in csv_files:
#      csv_path = os.path.join(csv_dir, csv_file)
#      df = pd.read_csv(csv_path)
# print(df)