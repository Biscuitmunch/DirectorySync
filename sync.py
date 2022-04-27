import datetime
from hmac import digest
from pathlib import Path
import json

#digest_dictionary = {filename: }

def Get_Modified_Time(path):
    return Path(path).stat().st_mtime

def Get_Digest_Dictionary(path):
    #return json.load(path + r'\.sync')
    return {}

def Save_Digest(path, file, modified):
    digest_dictionary = Get_Digest_Dictionary(path)

    if file in digest_dictionary:
        digest_dictionary[file].append([modified, 500])
        
    else:
        digest_dictionary[file] = [modified, 700]

    with open((str(path) + '.json'), 'w') as js:
        json.dump(digest_dictionary, js,  indent=4)

def Update_Digest(path):

    file_list = Path(path).glob('*')
    for file in file_list:
        
        if file.is_dir():
            Update_Digest(file)
        
        if file.is_file():
            modifiedTime = Get_Modified_Time(file)
            Save_Digest(path, file, modifiedTime)



def Compare_Digest(path):
    print("hello")

dir1User = input()
dir2User = input()

# path1
path1 = Path(dir1User)
Update_Digest(path1)


