import json

def load_data():
    try:
        with open('data/database.json','r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError:
        data = {}
    if 'users' not in data:
        data['users'] = []
    if 'logs' not in data:
        data['logs'] = []
    return data

def save_data(data):
    with open('data/database.json','w') as file:
        json.dump(data,file,indent=4)



def clear_data(data):
    data['users'] = []
    data['logs'] = []
    save_data(data)
