FROM ubuntu:14.04

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
#RUN sed -i s:/archive.ubuntu.com:/mirrors.aliyun.com/ubuntu:g /etc/apt/sources.list
RUN sed -i s:/archive.ubuntu.com:/mirrors.tuna.tsinghua.edu.cn/ubuntu:g /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN apt-get clean
RUN apt-get -y update --fix-missing

#编译安装 python3.6 所需组建
RUN apt-get -y install wget
RUN apt-get -y install gcc
RUN apt-get -y install build-essential
RUN apt-get -y install zlib*
RUN apt-get -y install openssl
RUN apt-get -y install libssl-dev
RUN apt-get -y install vim

#编译安装 python3.6.5
RUN mkdir /home/python \
    && cd /home/python \
    && wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz \
    && tar xfz Python-3.6.5.tgz \
    && cd Python-3.6.5 \
    && ./configure --prefix=/usr/bin/python3.6 \
    && sed -i 's/#_socket socketmodule.c/_socket socketmodule.c timemodule.c/g' Modules/Setup \
    && sed -i 's/#_ssl _ssl.c \\/_ssl _ssl.c \\/g' Modules/Setup \
    && sed -i '211i-DUSE_SSL -I$(SSL)/include -I$(SSL)/include/openssl \\' Modules/Setup \
    && sed -i '211a-L$(SSL)/lib -lssl -lcrypto' Modules/Setup \
    && ./configure --prefix=/usr/bin/python3.6 \
    && make \
    && make install \
#    && rm /usr/bin/python \
    && ln -s /usr/bin/python3.6/bin/python3.6 /usr/bin/python \
    && cd /

#安装pymysql
RUN python -m pip install pymysql

#启用cron日志
RUN sed  -i  's/#cron/cron/g' /etc/rsyslog.d/50-default.conf
VOLUME /var/log/

#创建脚本路径
RUN mkdir -p /home/scheduler
WORKDIR /home/scheduler

#安装MySQL
RUN apt-get -y install mysql-client
RUN apt-get -y install zip
RUN apt-get -y install unzip
RUN apt-get -y install rsyslog

RUN rsyslogd
RUN cron

#复制要运行的代码到镜像中，包括cron配置文件
COPY . /home/scheduler
RUN chmod -R 755 /home/scheduler

#复制crontabfile到/etc/crontab
RUN cp /home/scheduler/crontabfile /etc/crontab
RUN touch /var/log/cron.log

#设置cron脚本
RUN crontab /home/scheduler/crontabfile

#将run.sh设置为可执行
RUN chmod +x /home/scheduler/run.sh

WORKDIR /home/scheduler

# Run the command on container startup
#CMD rsyslogd && cron && tail -f /var/log/cron.log
CMD ["bash","/home/scheduler/run.sh"]