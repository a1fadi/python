import os 

source = "/import/reed/4/z5309136/comp1531/practice/arabic.txt"
destination = "/import/reed/4/z5309136/comp1531/"

try: 
    if os.path.exists(destination):
        print("NOOO")
    else:
        os.replace(source,destination)
        print("source was moved")
except Exception: