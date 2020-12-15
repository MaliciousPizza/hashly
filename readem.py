import json
from pprint import pprint
from main import md5_hash
from main import write_json
from main import get_digital_signature
from main import check_file_name
from main import check_file_type
from main import check_size


# all_your_datas = json.loads('all_your_datas.json')

with open('all_your_datas.json', 'r') as content_file:
    datas = content_file.read()

your_datas = json.loads(datas)

my_hash = your_datas["C:\\Program Files (x86)\\Microsoft\\EdgeUpdate\\1.3.137.99\\msedgeupdateres_cy.dll"]['file_hash']
new_hash = md5_hash("C:\\Program Files (x86)\\Microsoft\\EdgeUpdate\\1.3.137.99\\msedgeupdateres_cy.dll")

if my_hash == new_hash:
    print("hash matches")
else:
    print('hashes do not match')

try:

    pprint(your_datas[r"insert file name"])
except:
    file_path = r'insert file name'
    file_hash = md5_hash(file_path)
    file_size = check_size(file_path)
    file_type = check_file_type(file_path)
    file_name = check_file_name(file_path)
    digital_signature = get_digital_signature(file_path)
    with open('all_your_datas.json') as json_file:
        data = json.load(json_file)

        temp = data

        y = {r'insert file name':{
            'file_name' : file_name,
            'file_type' : file_type,
            'file_hash' : file_hash,
            'file_size' : file_size,
            'digital_signature' : digital_signature
        }}

        temp.update(y)
    write_json(data)

# print(all_your_datas["C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"])