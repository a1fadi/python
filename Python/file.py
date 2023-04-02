import os

path = "/import/reed/4/z5309136/comp1531/practice/omg.txt"

if os.path.exists(path):
    print ("SIUUU")
    if os.path.isfile(path):
        print ("thats a file")
    else:
        print ("no*2")
else:
    print("no")