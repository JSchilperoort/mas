class BluffSequence:
    def  __init__(self, action, agent, bluff_caller, bluff):
        self.action = str(action).replace("Actions.", "")
        self.agent = agent
        self.bluff_caller = bluff_caller
        self.bluff = bluff

    def agent_string(self):
        if self.bluff:
            return "Player bluffed his action"
        else:
            return ""
    def target_string(self):
        return "Player called bluff on Player {}'s action {}".format(self.agent.identifier, self.action)

    def result_string(self):
        if self.bluff:
            return "Player called the cluff correct and Player {} lost a card".format(self.agent.identifier)
            
        else:
            return "Player called the bluff wrongfully and lost a card"