from cockroaches import decontaminate

def generate_files(cockroaches):
    '''
    Input Parameters:

    - cockroaches        a dictionary of the form

    {
        'monday.txt': ['kitchen', 'attic', 'bathroom']
        'tuesday.txt': ['kitchen', 'bedroom', 'backyard'], etc
    }
    '''
    for filename in cockroaches:
        with open(filename, 'w') as FILE:
            for room in cockroaches[filename]:
                FILE.write(room + '\n')

def test_sample():
    files = ['monday.txt', 'friday.txt'] # E.G. Files are "monday.txt" and "friday.txt"
    # TODO: Create the test files and populate with data
    assert(decontaminate(files) == { 'backyard' : 1, 'kitchen' : 2 })
