FROM python:latest
#app.py api.py
COPY app /app
COPY run.sh /app/run.sh
WORKDIR /app
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \ 
	&& pip install PyJWT -i https://pypi.tuna.tsinghua.edu.cn/simple  \
	&& pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple \
	&& pip install flask -i https://pypi.tuna.tsinghua.edu.cn/simple 

RUN echo "c45g7580-1f4f-18he-b611-05j03e04d04m" > $(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)_FLAG
	
RUN chmod -R 777 /app
RUN chmod +x /app/run.sh

CMD [ "/app/run.sh"]

