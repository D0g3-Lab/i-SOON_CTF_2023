FROM php:7.3.4-apache

WORKDIR /var/www/html
COPY index.php /var/www/html/
COPY run.sh /
RUN chmod +x /run.sh
RUN chmod 777 /var/www/html/index.php
CMD ["/run.sh"]
