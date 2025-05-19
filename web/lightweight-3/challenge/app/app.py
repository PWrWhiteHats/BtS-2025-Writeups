import re
from flask import Flask, render_template, render_template_string, request
from ldap3 import Server, Connection, ALL
from subprocess import Popen, PIPE 

app = Flask(__name__)

ADMIN_PASSWORD = "STYE0P8dg55WGLAkFobiwMSJKix1QqpH"


@app.route('/search', methods=['GET'])
def search():
    prism = request.args.get('prism')

    if any(char in prism for char in [';']):
        return {
            'error': 'Bad characters detected'
        }

    cmd = f"ldapsearch -x -H ldap://localhost -b 'ou=prisms,dc=bts,dc=ctf' -D cn=admin,dc=bts,dc=ctf -s sub '(&(objectclass=prismProduct)(cn={prism}))' -w {ADMIN_PASSWORD}"
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return stderr.decode(), 500
    
    data = stdout.decode()

    image = re.search(r'prismImageURL: (.*)', data)
    if image:
        image = image.group(1)

    return {
        'data': data,
        'image': image
    }


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

        return render_template('index.html', username=username, description=conn.entries[0].description)
    
    return render_template('login.html')
