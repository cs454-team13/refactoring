class Country:

    def __init__(self, name):
        self.population = 0


class Korea(Country):

    def __init__(self, name):
        super(Country, self).__init__()
        self.name = name

    def get_name(self):
        return self.name


class China(Country):

    def __init__(self, name):
        super(Country, self).__init__()
