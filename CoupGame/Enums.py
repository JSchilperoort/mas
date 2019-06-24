from enum import Enum, auto

class AutoName(Enum):
    def _generate_next_value_(self, name, start, count, last_values):
        return name

class Influence(Enum):
    Ambassador = auto()
    Assassin = auto()
    Captain = auto()
    Contessa = auto()
    Duke = auto()

class Actions(Enum):
    # Default non blockable actions
    Income = auto()
    Coup = auto()
    # Blockable actions
    Foreign_Aid = auto()
    Swap_Influence = auto()
    Assasinate = auto()
    Steal = auto()
    Tax = auto()
    # Block actions
    Block_Steal = auto()
    Block_Assasinate = auto()
    Block_Foreign_Aid = auto()
