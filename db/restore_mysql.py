import os
import json
import sys
from pathlib import Path

script_path = Path(__file__).parent
in_conf_name = sys.argv[1]
restore_time = sys.argv[2]
# sql_path = script_path.joinpath("restore")
# if not os.path.exists(sql_path):
#     os.makedirs(sql_path)

f = open(script_path.joinpath('config.json'))
Config = json.loads(f.read())
f.close()
Config = Config['mysql_inf']

for _config in Config:
    conf_name = _config['name']
    if conf_name != in_conf_name:
        continue
    host = _config['host']
    user = _config['user']
    password = _config['password']
    dbname = _config['db']
    port = _config['port']
    charset = _config['charset']

    sql_path = f'{script_path}/{dbname}/{restore_time[0:6]}/{restore_time}'
    file_list = os.listdir(sql_path)
    if len(file_list) == 0:
        sys.exit(f"{sql_path}  目录下没有文件")
    for file in file_list:
        file_name = file[0:len(file)-20]
        file_suffix = file[len(file)-4:len(file)]

        if file_suffix == '.zip':
            linux_unzip = f"unzip -o '{sql_path}/{file}' -d '{sql_path}/'"
            os.system(linux_unzip)
            # os.remove(f'{sql_path}/{file}')
            file = file_name + '.sql'
        elif file_suffix != '.sql':
            continue
        linux_mysql = f"mysql --default-character-set=utf8  -h'{host}' -u'{user}' -p'{password}'" \
                      f" '{dbname}'< '{sql_path}/{file}'"
        os.system(linux_mysql)
        os.remove(f'{sql_path}/{file}')
