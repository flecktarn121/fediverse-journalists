class Entity:

    def __init__(self, name):
        self.name = name
        self.main_match = ''
        self.secondary_matches = set()
        self.frequency = 0
        self.description = ''
        self.label = ''
    