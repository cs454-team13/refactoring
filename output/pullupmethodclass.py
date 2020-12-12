class Country:

    def __init__(self):
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

    def __init__(self):
        super(Country, self).__init__()
        self.name = 'China'
