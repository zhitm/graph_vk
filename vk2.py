import json
from urllib.request import urlopen
from pprint import pprint

file1 = open('members.txt', 'r')
file2 = open('friends_of_members2.txt', 'w')

token = '5641c5e45641c5e45641c5e4f25633ab13556415641c5e4089bd500489a896d0d89892d'

ids = [int(line.strip()) for line in file1]
count = 0

for k in range(len(ids)):
    user_id = ids[k]
    url = f'https://api.vk.com/method/friends.get?v=5.107&user_id={user_id}&access_token={token}&count=1000'
    data = json.loads(urlopen(url).read())
    pprint(k)
    if not ('error' in data):
        file2.write(str(user_id) + ' ')
        for index in data['response']['items']:
            if index in ids:
                file2.write(str(index) + ' ')
        file2.write('\n')
    else:
        count +=1

file1.close()
file2.close()
print(count)
