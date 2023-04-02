days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def day_to_message(d):
    '''
    convert the day into a message, i.e for a passed in day argument, return the corresponding message for that day
    '''
    d = d.lower()
    #put all statements into a list
    statements = ["It's Monday!", "It's Tuesday! Exam DAY", "it's the middle of the work week!", " Almost friday...", "Rebecca who?", "yay weekend!", "almost monday :("]
    #find the corresponding statement to day
    for i in range(len(days)): 
        if days[i] == d:
            return statements[i]

if __name__ == '__main__':
    #list of all the days of the week 
    d = input("Enter the day of the week: ")
    #making them lowercase
    d = d.lower()
    #if input isnt a day of the week, exit
    if d not in days: 
        exit()

    print(day_to_message(d))
