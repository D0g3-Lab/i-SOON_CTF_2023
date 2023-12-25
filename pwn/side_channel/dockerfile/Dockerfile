FROM kalilinux/kali-rolling:latest
# RUN sudo echo "nameserver 8.8.8.8" > /etc/resolv.conf

RUN sed -i 's#http://http.kali.org/kali#http://mirrors.ustc.edu.cn/kali#g' /etc/apt/sources.list && \
    sed -i 's#http://security.kali.org/kali-security#http://mirrors.ustc.edu.cn/kali-security#g' /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd

RUN useradd -m ctf

WORKDIR /home/ctf

RUN   cp -R /usr/lib* /home/ctf

RUN mkdir /home/ctf/dev && \
    mknod /home/ctf/dev/null c 1 3 && \
    mknod /home/ctf/dev/zero c 1 5 && \
    mknod /home/ctf/dev/random c 1 8 && \
    mknod /home/ctf/dev/urandom c 1 9 && \
    chmod 666 /home/ctf/dev/*

RUN mkdir /home/ctf/bin && \
    cp /bin/sh /home/ctf/bin && \
    cp /bin/ls /home/ctf/bin && \
    cp /bin/cat /home/ctf/bin && \ 
    cp /bin/chmod /home/ctf/bin

COPY ./ctf.xinetd /etc/xinetd.d/ctf
COPY ./flag.sh /flag.sh
RUN echo "Blocked by ctf_xinetd" > /etc/banner_fail

RUN chmod +x /flag.sh

COPY ./bin/ /home/ctf/
RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 4755 /home/ctf/chall

CMD ["/flag.sh"]

