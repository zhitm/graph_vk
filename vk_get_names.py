import json
from urllib.request import urlopen
from pprint import pprint

file1 = open('members.txt', 'r')
file2 = open('members2.txt', 'w')

token = '5641c5e45641c5e45641c5e4f25633ab13556415641c5e4089bd500489a896d0d89892d'

ids = [int(line.strip()) for line in file1]

for k in range(len(ids)):
    user_id = ids[k]
    url = f'https://api.vk.com/method/users.get?v=5.107&user_id={user_id}&access_token={token}'
    data = json.loads(urlopen(url).read())
    
	try:
		file2.write(str(user_id) + data['response'][0]['first_name'] + data['response'][0]['last_name'] + '\n')
	
	except:
		file2.write(str(user_id) + "polish asshole" + '\n')

file1.close()
file2.close()
