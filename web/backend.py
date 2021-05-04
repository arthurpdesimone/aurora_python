import random
import string


from flask import request, Flask

from database.DatabaseManager import DatabaseManager
from database.User import User

app = Flask(__name__)


@app.route('/')
def home():
    return "Aurora backend version 0.1"


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        serial = request.args.get('serial')
        mac = request.args.get('mac')
        return do_login(serial,mac)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.args.get('name')
        email = request.args.get('email')
        cpf = request.args.get('cpf')
        mac = request.args.get('mac')
        return register_user(name,email,cpf,mac)


def do_login(serial, mac):
    """ Create the individual database """
    db = DatabaseManager(serial+'.json')
    return "Banco de dados criado"


def register_user(name,email,cpf,mac):
    serial = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    db = DatabaseManager('database.json')
    user = User(name,email,cpf,serial,mac)
    success = db.create_user(user)
    if success:
        return "Usuário já existe"
    else:
        return "Usuário criado"

if __name__ == '__main__':
    app.run()