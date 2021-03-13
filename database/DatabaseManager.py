from math import sqrt

from tinydb import TinyDB, Query


class DatabaseManager:
    """ Create a database manager """

    def __init__(self, file):
        self.db = TinyDB(file, indent=4, separators=(',', ': '))
        self.db.table('materials')
        self.create_standard_materials()

    def create_standard_materials(self):
        """ Create both steel and concrete materials according to the brazilian standards

            The standard adopted for concrete is NBR 6118:2007 TODO Update to NBR 6118:2020
            https://www.phd.eng.br/wp-content/uploads/2014/06/269.pdf

        """

        """ Concrete creation """
        if len(self.db.table('materials')) == 0:
            for i in range(1, 6):
                type = "Concrete"
                name = "C" + str(i * 10)
                fck = i * 10000000.0
                young_modulus_tangent = 5600 * sqrt(fck) #TODO Correct the formula to GPa
                young_modulus_secant = 0.85 * young_modulus_tangent
                dilatation_coefficient = 0.00001
                yield_strain = 0.002
                rupture_strain = 0.0035
                self.db.table('materials').insert({"type": type,
                                                   "name": name,
                                                   "fck": fck,
                                                   "young_modulus_tangent": young_modulus_tangent,
                                                   "young_modulus_secant": young_modulus_secant,
                                                   "dilatation_coefficient": dilatation_coefficient,
                                                   "yield_strain": yield_strain,
                                                   "rupture_strain": rupture_strain
                                                   })
