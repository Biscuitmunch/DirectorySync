from array import array
from hmac import digest
from pathlib import Path
import json
import hashlib

def Create_Hash(path):
    # Hashing the data as a hex digest
    with open(path, 'rb') as file:
        data = file.read()
        return str(hashlib.sha256(data).hexdigest());

def Get_Modified_Time(path):
    return Path(path).stat().st_mtime

def Get_Digest_Dictionary(path):
    # check if exists
    if Path.exists(Path(path)):
        with open(path) as js:
            return json.load(js)
    else:
        return {}


def Save_Digest(path, file):
    modified = Get_Modified_Time(file)
    file_hash = Create_Hash(file)

    # json file locations
    path_for_json = str(path)
    array_of_paths = path_for_json.split('/')
    final_name = array_of_paths[-1]
    json_path_complete = path_for_json + '/.' + final_name + '.json'

    digest_dictionary = Get_Digest_Dictionary(json_path_complete)

    file_name = str(file)

    # Adding specific file to the dictionary which will be the .json file
    if file_name in digest_dictionary:
        digest_dictionary[file_name].append([modified, file_hash])
    
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
        
        # If it is a directory, we recursively run this again to get that digest
        if file.is_dir():
            Update_Digest(file)
        
        # Otherwise, perform normal actions
        if file.is_file():
            Save_Digest(path, file)



def Compare_Digest(path):
    print("hello")

dir1User = input()
dir2User = input()

# path1
path1 = Path(dir1User)
Update_Digest(path1)


