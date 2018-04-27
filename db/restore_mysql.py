import os
import json
import sys
from pathlib import Path

script_path = Path(__file__).parent

sql_path = script_path.joinpath("restore")
if not os.path.exists(sql_path):
    os.makedirs(sql_path)

file_list = os.listdir(sql_path)
if len(file_list) == 0:
    sys.exit("db/restore目录下没有文件")

f = open(script_path.joinpath('config.json'))
Config = json.loads(f.read())
f.close()
Config = Config['restore_mysql_inf'][0]

host = Config['host']
user = Config['user']
password = Config['password']
dbname = Config['db']
port = Config['port']
charset = Config['charset']

for file in file_list:
    file_name = file[0:len(file)-20]
    file_suffix = file[len(file)-4:len(file)]

    if file_suffix == '.zip':
        linux_unzip = f"unzip -o '{sql_path}/{file}' -d '{sql_path}/'"
        os.system(linux_unzip)
        os.remove(f'{sql_path}/{file}')
        file = file_name + '.sql'
    elif file_suffix != '.sql':
        continue
    linux_mysql = f"mysql --default-character-set=utf8  -h'{host}' -u'{user}' -p'{password}'" \
                  f" '{dbname}'< '{sql_path}/{file}'"
    os.system(linux_mysql)
    os.remove(f'{sql_path}/{file}')
