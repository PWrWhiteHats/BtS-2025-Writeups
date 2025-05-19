#!/bin/bash

# append description with flag
echo "description: BtSCTF{${FLAG_PREFIX}_bl1nd_ld4p_1nj3ct10n_y1pp333333}" >> /base.ldif && cat /base.ldif

# start
echo Starting
service slapd start

sleep 1
ldapadd -D cn=admin,dc=bts,dc=ctf -f /base.ldif -x -w STYE0P8dg55WGLAkFobiwMSJKix1QqpH

cd /app && python3 -m gunicorn -b 0.0.0.0:80 app:app
