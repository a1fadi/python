try:
    numerator = int(input("please enter a numerator: "))
    denominator = int(input("please enter a denominator: "))
    result = numerator/denominator 
except ZeroDivisionError as e:
    print(e)
    print("why u diving by zero clown?")
except ValueError as e:
    print(e)
    print("NO!")
else: 
    print(result)
finally: 
    print("goottrydash")