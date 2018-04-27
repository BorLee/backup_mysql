# 使用环境
ubuntu 16 + python 3.6 或者 docker
# 功能介绍
- 备份 mysql 指定库里各个表和函数
- 每个表会单独压缩成 zip 格式
- 所有函数最后会压缩成一个 procedure_and_function-date.zip
- 可配置多个数据库
- 支持 docker

# 备份文件存放示例

db/dbname/201804/20180421/table-20180421-00:00:00.zip

# 使用
```
git clone https://github.com/BorLee/backup_mysql.git
cd backup_mysql
mv db/config_sample.json db/config.json
vi db/config.json
```
> config.json 说明
>
> mysql_inf: 备份配置
>
> restore_mysql_inf: 恢复配置
>
> 多个数据库用 , 隔开，默认 config 是备份两个库的示例。

docker 运行
```
sudo docker build -t backup_mysql:py3.6 .
sudo docker run -d backup_mysql:py3.6
```

直接运行脚本
```
python db/back_db.py
```

# 恢复数据库脚本使用
把 zip 备份文件全部移动到 db/restore 目录下
```
python db/restore_mysql.py
```