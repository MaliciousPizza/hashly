import hashlib
import sys
import filetype
import subprocess
import json
import pprint
from os import path
from os.path import splitext
from os.path import basename
from os.path import join
from os.path import dirname
from os.path import getsize
from os import walk
from os import stat

#set up something to enumerate through a directory and save the directory contents to a list
def enumerate_directory(d):
    for path, currentDirectory, files in walk(d):
        for file in files:
            return  join(path,file)

# Grabs the MD5 hash of a file that is pushed to it. 
def md5_hash(m):
    BLOCKSIZE = 65536
    md5 = hashlib.md5()
    with open(m,'rb') as file_to_hash:
        while True:
            buffer = file_to_hash.read(BLOCKSIZE)
            if not buffer:
                break
            md5.update(buffer)
    return md5.hexdigest()

#checks the size of the file. hopefully to notice if a file size has changed. should indicate if it has been rewritten. 
def check_size(m):
    # file_size = getsize(m)
    file_size = stat(m).st_size
    return file_size

#returns the file type. by looking at the mimetype. if no mimetype is found returns just the extension
def check_file_type(m):
    file_type = filetype.guess(m)
    if file_type is None:
        file_ext = str(m).split('.')[-1]
        return file_ext
    return file_type.mime

#gets the file name from the file to save in the DB
def check_file_name(m):
    base_name = basename(m)
    file_name = splitext(base_name)[0]
    return file_name

#uses sysinternals sigcheck to get the digital signature of the file. 
def get_digital_signature(m):
    try:
        signature = subprocess.check_output('C:\SysinternalsSuite\sigcheck.exe "{}"'.format(m))
        signature = signature.decode('utf-8')
        sig_dict = {}
        for row in signature.split('\r\n\t'):
            if ':\t' in row:
                key,value = row.split(':\t')
                sig_dict[key.strip(':\t')] = value.strip()
        return '{} by {}'.format(sig_dict['Verified'],sig_dict['Publisher'])
    except:
        return 'Unsigned file'

def write_json(data, filename):
    """
        writes the data to json file.
        Requires the data to be formatted as a dictionary as well 
        as the filename you hope to update 
        
        syntax = write_json(<data>,<filename>)    
    """
    with open(filename,'w') as f:
        json.dump(data,f,indent=4,sort_keys=True)    

#creates the baseline for the hashes and saves it to a file named baselin_hashes.json
def create_baseline_hashes(d):
    dictionary = {}

    with open('baseline_hashes.json','w+') as json_file:
        for path, currentDirectory, files in walk(d):
            for the_file in files:
                file_path = join(path,the_file)
                file_hash = md5_hash(file_path)
                file_size = check_size(file_path)
                file_type = check_file_type(file_path)
                file_name = check_file_name(file_path)
                digital_signature = get_digital_signature(file_path)

                dictionary.update({file_path:{
                    'file_name': file_name,
                    'file_type': file_type,
                    'file_hash': file_hash,
                    'file_size' : file_size,
                    'digital_signature' : digital_signature
                }})

        json.dump(dictionary,json_file, indent=4, sort_keys=True)


#TODO: def PE File distinction

#TODO: NSRL lookup

#Check Hash against hash json baseline database
def get_hash_from_baseline(d):
    with open('baseline_hashes.json', 'r') as content_file:
        datas = content_file.read()

    your_datas = json.loads(datas)

    return your_datas[d]['file_hash']


if __name__ == '__main__':


    print(get_hash_from_baseline(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"))

    
