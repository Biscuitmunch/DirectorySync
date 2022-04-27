import datetime
from pathlib import Path

#digest_dictionary = {filename: }

def Get_Modified_Time(path):
    return Path(path).stat().st_mtime

def Digest_Dictionary(path):
    print("hello")

def Compare_Digest(path):
    print("hello")

def Add_To_Digest(path):
    file_list = Path(path).glob('*')
    for i in file_list:
        modifiedTime = Get_Modified_Time(i)
        print(modifiedTime)

dir1User = input()
dir2User = input()

# path1 and path1 files
path1 = Path(dir1User)
Add_To_Digest(path1)


