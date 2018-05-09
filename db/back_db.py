import os
import json
import pymysql
import datetime
from pathlib import Path

now = datetime.datetime.now()
today = datetime.date.today()
# yesterday = now - datetime.timedelta(days=1)
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")
time = now.strftime("%Y%m%d-%H%M%S")

# 脚本执行路径/备份存放点
# script_path = os.getcwd()
script_path = Path(__file__).parent
f = open(script_path.joinpath('config.json'))
Config = json.loads(f.read())
f.close()

Config = Config['mysql_inf']

for _config in Config:
    host = _config['host']
    user = _config['user']
    password = _config['password']
    dbname = _config['db']
    port = _config['port']
    charset = _config['charset']

    back_path = f'{script_path}/{dbname}/{year}{month}/{year}{month}{day}'

    if not os.path.exists(back_path):
        os.makedirs(back_path)

    db = pymysql.connect(host=host, user=user, password=password, db=dbname, port=port, charset=charset)
    cursor = db.cursor()

    cursor.execute("show tables")
    tables = cursor.fetchall()

    for Table in tables:
        table = Table[0]

        linux_dump = f"mysqldump --default-character-set=utf8" \
                     f" -h'{host}' '{dbname}' '{table}' -u'{user}' -p'{password}' > '{back_path}/{table}.sql'"
        os.system(linux_dump)

        linux_zip = f"zip -m -j {back_path}/{table}-{time}.zip {back_path}/{table}.sql"
        os.system(linux_zip)

    linux_dump_procedure = f"mysqldump --default-character-set=utf8 -h'{host}' -u'{user}'" \
                           f" -p'{password}' -ntd -R  '{dbname}' > '{back_path}/procedure_and_function.sql'"
    os.system(linux_dump_procedure)
    linux_zip_procedure = f"zip -m -j {back_path}/procedure_and_function-{time}.zip" \
                          f" {back_path}/procedure_and_function.sql"
    os.system(linux_zip_procedure)
    db.close()
