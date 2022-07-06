import requests


HOST = 'http://127.0.0.1:8080/'


# response = requests.get(HOST + 'ads/2')
# response = requests.post(HOST + 'new_adv',
#                          json={'title': 'qwert', 'description': 'qwerty', 'owner': 'qwerty'})

# response = requests.delete(HOST + '/ads/del/1')
response = requests.put(HOST + '/ads/edit/2',
                        json={'title': 'gfggf', 'description': 'fgdgdd'})

print(response.status_code)
print(response.text)
