from enum import Enum, auto


class PersonState(Enum):
    untouched = auto()
    infected = auto()
    recovered = auto()  # And assumed to be immune
    deceased = auto()
    
    @classmethod
    def all(cls):
        return {cls.untouched, cls.infected, cls.recovered, cls.deceased}
