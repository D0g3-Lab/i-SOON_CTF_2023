#!/bin/sh
# Add your startup script
#!/bin/sh
echo $ICTF > /home/ctf/flag
unset ICTF
chmod 000 /home/ctf/flag
# DO NOT DELETE
/etc/init.d/xinetd start;
sleep infinity;
