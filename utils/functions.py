import json


def check_data(json_data):
    if 'abstention' not in json_data:
        json_data['abstention'] = "0"
    return json_data

def check_n_places(json_n_places):
    if 'n_places' not in json_n_places:
        json_n_places['n_places'] = "1"
        return json_n_places
    elif json_n_places['n_places'] == "0":
        json_n_places['n_places'] = "1"
    return json_n_places

def load_data(file_path='data.json'):
    try:
        with open(file_path, 'r') as data:
            election_data = json.load(data)
    except:
        election_data = {}        
        
    election_data = check_data(election_data)   
    return election_data

def save_data(data_dic, file_path='data.json'):        
    with open(file_path, 'w') as data:
        json.dump(data_dic, data)
        

def finish_init():
    pass