import json
from urllib.request import urlopen
from pprint import pprint

file = open('members.txt', 'w')
token = '5641c5e45641c5e45641c5e4f25633ab13556415641c5e4089bd500489a896d0d89892d'
for k in range(13):
    offset = k*1000
    url = f'https://api.vk.com/method/groups.getMembers?v=5.107&group_id=45&access_token={token}&offset={offset}&count=1000'
    data = json.loads(urlopen(url).read())
    pprint(k)
    for index in data['response']['items']:
        file.write(str(index) + '\n')

file.close()
