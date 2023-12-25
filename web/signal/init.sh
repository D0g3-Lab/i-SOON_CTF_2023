#!/bin/sh
echo $ICTF > /flag
chmod 444 /flag
unset ICTF
node /app/app.js