capitals = {'USA': 'Washington DC',
            'India': 'New Delhi',
            'China': 'Beijing',
            'Russia': 'Moscow'}
    
#print(capitals['Russia'])

#print(capitals.get('Russia'))

#cap = capitals.get('Russia')
#print(cap)

#print(capitals.keys())
#print(capitals.items())
#print(capitals.values())

capitals.update({'Germany': 'Berlin'})
capitals.update({'USA': 'Las Vegas'})
capitals.pop('USA')
#capitals.clear()

for key, value in capitals.items():
    print(key, value)





