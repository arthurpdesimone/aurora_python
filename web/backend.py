import random
import string


from flask import request, Flask, jsonify

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
    db = DatabaseManager('database.json')
    success = db.check_serial_and_mac(serial,mac)
    if success:
        return jsonify(message=serial, status=200)
    else:
        return jsonify(message="Serial ou mac invalidos", status=403)


def register_user(name,email,cpf,mac):
    """ Method to create a user """
    serial = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    db = DatabaseManager('database.json')
    user = User(name,email,cpf,serial,mac)
    success = db.create_user(user)
    if success:
        return jsonify(message = "Usuário já existe",status=403)
    else:
        return jsonify(message = serial ,status = 200)



if __name__ == '__main__':
    app.run()