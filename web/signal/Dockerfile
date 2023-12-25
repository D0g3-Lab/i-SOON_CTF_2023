FROM node:18.18.0

WORKDIR /app
COPY ./package.json ./package-lock.json ./
RUN npm install
COPY ./app /app
COPY ./readflag /readflag
RUN chmod 111 /readflag
COPY ./init.sh ./init.sh
RUN chmod +x /app/init.sh

CMD ["/app/init.sh"]
