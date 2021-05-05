import os
from math import sqrt
from tinydb import TinyDB, Query

from model.Material import Material


class DatabaseManager:
    """ Create a database manager """
    def __init__(self, file):
        if os.path.isfile(file):
            self.db = TinyDB(file, indent=4, separators=(',', ': '))
        else:
            self.db = TinyDB(file, indent=4, separators=(',', ': '))
            self.db.table('materials')
            self.create_standard_materials()

    def create_user(self, user):
        """ Method to receive a User and to store it if CPF(unique number) is not present"""
        user_query = Query()
        result = self.db.table('user').contains(user_query.email == user.email)
        if not result: self.db.table('user').insert(user.to_JSON())
        return result

    def check_serial_and_mac(self,serial,mac):
        serial_query = Query()
        mac_query = Query()
        result_serial = self.db.table('user').contains(serial_query.serial == serial)
        result_mac = self.db.table('user').contains(mac_query.mac == mac)
        return result_mac and result_serial

    def create_standard_materials(self):
        """ Create both steel and concrete materials according to the brazilian standards

            The standard adopted for concrete is NBR 6118:2007 TODO Update to NBR 6118:2020
            https://www.phd.eng.br/wp-content/uploads/2014/06/269.pdf

        """
        material_query = Query()

        for i in range(1, 6):
            type = "Concrete"
            name = "C" + str(i * 10)
            fck = i * 10000000.0
            young_modulus_tangent = 5600 * sqrt(fck)  #TODO Correct the formula to GPa
            young_modulus_secant = 0.85 * young_modulus_tangent
            dilatation_coefficient = 0.00001
            yield_strain = 0.002
            rupture_strain = 0.0035

            concrete = Material(name=name,
                                type=type,
                                fck=fck,
                                young_modulus_tangent=young_modulus_tangent,
                                young_modulus_secant=young_modulus_secant,
                                dilatation_coefficient=dilatation_coefficient,
                                yield_strain=yield_strain,
                                rupture_strain=rupture_strain)
            """ Update table materials """
            self.db.table('materials').upsert(concrete.to_JSON(),material_query.name == name)
