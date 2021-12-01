import requests

data = {
    'sum': 1000000,
    'rate': 12.0,  # per Year
    'date1': '01.01.2019',
    'date2': '01.01.2020',
    'simple': False
}

r = requests.post('http://localhost:8000', json=data)
# r = requests.post('http://localhost:8000/api', data={'key': 'value'})
print('status:', r.status_code)
print('json:', r.json())
