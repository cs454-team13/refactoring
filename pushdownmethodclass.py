class Country:

    def __init__(self):
        self.name = name
        self.population = 0

    def get_name(self):
        return self.name


class Korea(Country):

    def __init__(self):
        super(Country, self).__init__()
        self.name = 'Korea'
    
    def hi(self):
        return self.get_name()


class China(Country):
    name = 'China'

    def __init__(self):
        super(Country, self).__init__()
        self.name = 'China'

