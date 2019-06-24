class BluffSequence:
    def  __init__(self, action, agent, bluff_caller, bluff, belief):
        self.action = str(action).replace("Actions.", "")
        self.agent = agent
        self.bluff_caller = bluff_caller
        self.bluff = bluff
        self.belief = belief

    def agent_string(self, counter):
        if self.belief:
            return "{}. Player believes the action is valid\n".format(counter)
        else:
            return "{}. Players beliefs Player {} is bluffing\n".format(counter, self.agent.identifier+1)
        
    def result_string(self, counter):
        if self.belief:
            return ""
        else:
            if self.bluff:
                return "{}. Bluff call was correct so Player {} loses a card\n".format(counter, self.agent.identifier+1)       
            else:
                return "{}. Player called the bluff wrongfully and lost a card\n".format(counter)