import json
import os

DATA_FILE = 'data.json'
DEFAULT_DATA = {
    'clients': [
        {'id': 1, 'name': 'Oksana', 'phone': '8913'}
    ]
}


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f)


if __name__ == '__main__':
    data = load_data()
    print(data)
    data['clients'].append({'id': 2, 'name': 'Kris', 'phone': '8929'})
    save_data(data)
    print(data)
