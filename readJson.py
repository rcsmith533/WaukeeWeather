import json

with open('5Day.txt') as json_file:
    data = json.load(json_file)
    print(data['cod'])
    print('-------')
    print(data['message'])
    print('-------')
    print(data['cnt'])
    print('-------')
    print(data['list'])
    print('-------')
    print(data['city'])
    print('--------------------------------------------------')
    for i in data['list']:
        print(i['dt_txt'])