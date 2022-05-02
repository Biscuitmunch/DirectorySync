from array import array
from hmac import digest
import os
from pathlib import Path
import json
import hashlib
from pickle import FALSE
import shutil
import sys

def Create_Hash(path):
    # Hashing the data as a hex digest
    with open(path, 'rb') as file:
        data = file.read()
        return str(hashlib.sha256(data).hexdigest());

def Get_Modified_Time(path):
    return Path(path).stat().st_mtime

def Get_Accessed_Time(path):
    return Path(path).stat().st_atime

def Get_Digest_Dictionary(path):
    # check if exists
    if Path.exists(Path(path)):
        with open(path) as js:
            return json.load(js)
    else:
        return {}

def Add_To_Dictionary(digest_dictionary, file_name, modified, file_hash):

    if file_name in digest_dictionary:
        digest_dictionary[file_name].insert(0,[modified, file_hash])
    
    # If it was not there, we create it
    else:
        digest_dictionary[file_name] = [[modified, file_hash]]

    return digest_dictionary

def Save_Digest(path, file):
    modified = Get_Modified_Time(file)
    file_hash = Create_Hash(file)
    accessed = Get_Accessed_Time(file)

    # json file locations
    path_for_json = str(path)
    # array_of_paths = path_for_json.split('/')
    # final_name = array_of_paths[-1]
    json_path_complete = path_for_json + '/.' + 'sync' + '.json'

    digest_dictionary = Get_Digest_Dictionary(json_path_complete)

    file_name = str(file)

    # Adding specific file to the dictionary which will be the .json file
    if file_name in digest_dictionary:
        print(digest_dictionary[file_name][0][0])
        if (digest_dictionary[file_name][0][1] == file_hash):
            os.utime(file_name, (accessed, digest_dictionary[file_name][0][0]))
        else:
            digest_dictionary[file_name].insert(0,[modified, file_hash])
    
    # If it was not there, we create it
    else:
        digest_dictionary[file_name] = [[modified, file_hash]]

    # Dumping the new data to the .json file
    with open(json_path_complete, 'w') as js:
        json.dump(digest_dictionary, js,  indent=4)
        js.close()

def Update_Digest(path):

    # Iterating all files
    file_list = Path(path).glob('*')
    for file in file_list:

        # Make sure it is not a hidden file
        file_name_split = str(file).split('/')
        if file_name_split[-1][0] == '.': # If hidden file we skip to next file
            continue
        
        # If it is a directory, we recursively run this again to get that digest
        if file.is_dir():
            Update_Digest(file)
        
        # Otherwise, perform normal actions
        if file.is_file():
            Save_Digest(path, file)

def Remove_Hiddens(path):
    # Iterating all files
    file_list = Path(path).glob('*')
    for file in file_list:

        # If hidden file, we delete
        file_name_split = str(file).split('/')
        if file_name_split[-1][0] == '.': # If hidden file we skip to next file
            os.remove(str(file))
        
        # If it is a directory, check next layer down
        if file.is_dir():
            Remove_Hiddens(file)

#def Copy_And_Replace(src_path, dest_path):


def Compare_Digest(path1, path2):
    path1_for_json = str(path1)
    json_path1 = path1_for_json + '/.' + 'sync' + '.json'
    path1_dictionary = Get_Digest_Dictionary(json_path1)

    path2_for_json = str(path2)
    json_path2 = path2_for_json + '/.' + 'sync' + '.json'
    path2_dictionary = Get_Digest_Dictionary(json_path2)

    for key1, value1 in path1_dictionary.items():
        for key2, value2 in path2_dictionary.items():

            name1 = key1.split('/')[-1]
            name2 = key2.split('/')[-1]

            if (name1 == name2):
                # Check if file same digest
                if (value1[1] == value2[1]):
                    # Compare modification Dates
                    if (value1[0] > value2[0]):
                        print('1 bigger')

                    

            else:
                print('not')
        

path1 = Path(sys.argv[1])
path2 = Path(sys.argv[2])

if (path1.is_dir == False and path2.is_dir == False):
    print("Both Invalid Directories")
    quit()
    
if (path1 == path2):
    print("Same Directory!")
    quit()

if (path1.is_dir() == True and path2.exists() == False):
    shutil.copytree(str(path1), str(path2))
    Remove_Hiddens(path2)
    Update_Digest(path1)
    Update_Digest(path2)
    quit()

if (path2.is_dir() == True and path1.exists() == False):
    shutil.copytree(str(path2), str(path1))
    Remove_Hiddens(path1)
    Update_Digest(path1)
    Update_Digest(path2)
    quit()

# Path1
Update_Digest(path1)

# Path2
Update_Digest(path2)

# Deleted File Check
Compare_Digest(path1, path2)