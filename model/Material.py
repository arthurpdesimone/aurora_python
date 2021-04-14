import json


class Material:
    """ Class to define a material """
    def __init__(self,**kwargs):
        """ https://stackoverflow.com/questions/2535917/how-do-i-copy-kwargs-to-self """
        vars(self).update(kwargs)
        if 'name' not in kwargs:
            raise ValueError("Parameter name required")
        if 'type' not in kwargs:
            raise ValueError("Parameter type required")


    def to_JSON(self):
        return json.loads(json.dumps(self,default=lambda o:o.__dict__))