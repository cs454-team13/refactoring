class Country:

    def __init__(self):
        self.population = 0
        self.name = None


class Korea(Country):

    def __init__(self):
        super(Country, self).__init__()
        self.name = 'Korea'

    def get_name(self):
        return self.name


class China(Country):

    def __init__(self):
        super(Country, self).__init__()
        self.name = 'China'
