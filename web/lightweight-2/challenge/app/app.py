from flask import Flask, render_template, render_template_string, request
from ldap3 import Server, Connection, ALL
import os

FLAG_PREFIX = os.getenv('FLAG_PREFIX')
if FLAG_PREFIX is None:
    raise EnvironmentError("FLAG_PREFIX not set")

app = Flask(__name__)
app.secret_key = "BtSCTF{" + FLAG_PREFIX + "_ld4p_1nj3ction_plus_sst1_3quals_fl4g}"

ADMIN_PASSWORD = "STYE0P8dg55WGLAkFobiwMSJKix1QqpH"


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        server = Server('localhost', port=389, get_info=ALL)

        conn = Connection(server, 
                          user=f'cn=admin,dc=bts,dc=ctf',
                          password=ADMIN_PASSWORD,
                          auto_bind=True)
        
        if not conn.bind():
            return 'Failed to connect to LDAP server', 500

        conn.search('ou=people,dc=bts,dc=ctf', f'(&(employeeType=active)(uid={username})(userPassword={password}))', attributes=['uid', 'description'])

        if not conn.entries:
            return 'Invalid credentials', 401

        with open('templates/index.html', 'r') as file:
            content = file.read()
            if '%username%' in content:
                content = content.replace('%username%', username)
            if '%description%' in content:
                content = content.replace('%description%', conn.entries[0].description.value)

            return render_template_string(content)
    
    return render_template('login.html')
