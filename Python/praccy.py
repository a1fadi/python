def praccy(integer): 
    try:
        result = sum(range(integer + 1))
    except TypeError:
        return 0 
    return result
    
if __name__ == "__main__":
    print(praccy(1213))