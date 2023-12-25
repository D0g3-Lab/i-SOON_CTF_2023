#!/bin/bash

echo $ICTF > /flag
sed -i '284978r /flag' /var/www/html/admin.php
unset ICTF
rm /flag
apache2-foreground
