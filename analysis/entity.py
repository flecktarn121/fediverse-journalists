class Entity:

    def __init__(self, name):
        self.name = name
        self.main_match = ''
        self.secondary_matches = set()
        self.frequency = 0
        self.description = ''
        self.label = ''
    
    def to_dict(self):
        return {
            'name': self.name,
            'label': self.label,
            'main_match': self.main_match,
            'description': self.description,
        }
    