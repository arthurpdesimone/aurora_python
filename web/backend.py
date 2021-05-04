from flask import request, Flask

from database.DatabaseManager import DatabaseManager

app = Flask(__name__)


@app.route('/')
def home():
    return "Aurora backend version 0.1"


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        serial = request.args.get('serial')
        mac = request.args.get('mac')
        return do_the_login(serial,mac)


def do_the_login(serial, mac):
    """ Create the individual database """
    db = DatabaseManager(serial+'-'+mac+'.json')
    return "Banco de dados criado"


if __name__ == '__main__':
    app.run()