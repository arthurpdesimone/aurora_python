from flask import request, Flask

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
    return serial + '-' + mac


if __name__ == '__main__':
    app.run()