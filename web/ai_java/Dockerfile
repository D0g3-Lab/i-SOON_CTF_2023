# 使用官方 Ubuntu 镜像作为基础
FROM ubuntu

# 设置国内镜像源
RUN sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list


# 添加国内 DNS 配置
#RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
RUN echo "nameserver 223.6.6.6" >> /etc/resolv.conf
# 更新软件包索引并安装一些基本软件
# 安装 MySQL 5.7
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server && \
    apt-get install -y mysql-client && \
    apt-get install -y cowsay && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
 
# 将 MySQL 运行时的配置文件复制到容器中
COPY my.cnf /etc/mysql/my.cnf
COPY init.sql /init.sql
COPY start.sh  /start.sh
COPY  ctf-0.0.1-SNAPSHOT.jar /ctf-0.0.1-SNAPSHOT.jar
RUN chmod +x /start.sh
COPY flag.sh /flag.sh
RUN chmod +x /flag.sh
COPY ./java /java



# 启动 MySQL 服务
CMD ["/start.sh"]
