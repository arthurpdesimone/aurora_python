import json


class User():
    def __init__(self, name, email, cpf, serial, mac):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.serial = serial
        self.mac = mac

    def to_JSON(self):
        return json.loads(json.dumps(self,default=lambda o:o.__dict__))