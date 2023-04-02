def hello(**kwargs):
    print(f"Wassup", end = " ")
    for i  in kwargs:
        print(kwargs[i], end = " ")

(hello(first = 'fadi', last = 'beast', second = 'hatu', third = 'nigga'))