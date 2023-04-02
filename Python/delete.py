import os 
import shutil 

path = '/import/reed/4/z5309136/comp1531/practice/folder1/'

try:
    shutil.rmtree(path) 
except Exceptions:
    print('you cant do that')
