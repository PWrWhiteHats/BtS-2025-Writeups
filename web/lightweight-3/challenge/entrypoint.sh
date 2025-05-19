#!/bin/bash

echo "BtSCTF{${FLAG_PREFIX}_gl4d_t0_s33_y0u_g0t_output_out_of_th3_comm4nd_1nj3ction}" > /root/flag.txt

cd /app/
echo Starting
/usr/sbin/service slapd start

sleep 1

ldapadd -Q -Y EXTERNAL -H ldapi:/// -f add-prism-schema.ldif
ldapadd -D cn=admin,dc=bts,dc=ctf -f base.ldif -x -w STYE0P8dg55WGLAkFobiwMSJKix1QqpH

sudo -u prism python3 -m gunicorn -b 0.0.0.0:8080 app:app
