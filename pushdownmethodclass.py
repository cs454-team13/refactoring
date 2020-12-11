class Country:

    def __init__(self, name):
        self.name = name
        self.population = 0

    def get_name(self):
        return self.name

class Korea(Country):

    def __init__(self, name):
        super(Country, self).__init__()
    
class China(Country):
    
    def __init__(self, name):
        super(Country, self).__init__()

